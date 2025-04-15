from __future__ import annotations

import os
import platform
import re
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any
from urllib import request

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class SpecialBuildHook(BuildHookInterface):
    BIN_NAME = "yamlfmt"
    YAMLFMT_REPO = "https://github.com/google/yamlfmt/releases/download/v{version}/yamlfmt_{version}_{target_os_info}_{target_arch}.tar.gz"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temp_dir = Path(tempfile.mkdtemp())

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        # 仅在构建 Wheel 文件时执行此逻辑
        if self.target_name != "wheel":
            return

        target_arch = os.environ.get("CIBW_ARCHS", platform.machine()).lower()
        target_os_info = os.environ.get("CIBW_PLATFORM", sys.platform).lower()

        if target_arch not in ["x86_64", "arm64", "aarch64"]:
            raise NotImplementedError(f"no support arch: {target_arch}")

        if not any(os_name in target_os_info for os_name in ["linux", "darwin", "macos", "win"]):
            raise NotImplementedError(f"no support os: {target_os_info}")

        # 检查系统和架构的组合
        if target_os_info in ["win"] and target_arch == "x86_64":
            target_arch = "amd64"
        elif target_os_info in ["linux"] and target_arch == "arm64":
            target_arch = "aarch64"
        if target_os_info in ["darwin", "macos"]:
            target_os_info = f"macosx_{'10_9' if target_arch == 'x86_64' else '11_0'}"
            if target_arch == "aarch64":
                target_arch = "arm64"

        # 构建完整的 Wheel 标签
        full_wheel_tag = f"py3-none-{target_os_info}_{target_arch}"
        build_data["tag"] = full_wheel_tag

        # 下载 yamlfmt 可执行文件
        tar_gz_file = self.download_yamlfmt(target_os_info, target_arch)

        # 解压缩文件
        with tarfile.open(tar_gz_file, "r:gz") as tar:
            if target_os_info == "win":
                # Windows 上的文件名是 yamlfmt.exe
                assert f"{self.BIN_NAME}.exe" in tar.getnames()
                tar.extract(f"{self.BIN_NAME}.exe", path=self.temp_dir)
                # 重命名为 yamlfmt
                (self.temp_dir / f"{self.BIN_NAME}.exe").rename(self.temp_dir / self.BIN_NAME)
            else:
                assert self.BIN_NAME in tar.getnames()
                tar.extract(self.BIN_NAME, path=self.temp_dir)

        # TODO: 加一个 sum 校验
        bin_path = self.temp_dir / self.BIN_NAME
        assert bin_path.is_file(), f"{self.BIN_NAME} not found"
        build_data["force_include"][f"{bin_path.resolve()}"] = f"yamlfmt/{self.BIN_NAME}"

    def download_yamlfmt(self, target_os_info: str, target_arch: str) -> None:
        """Download the yamlfmt binary for the specified OS and architecture."""
        target_os_info_to_go_os = {
            "macosx_10_9": "Darwin",
            "macosx_11_0": "Darwin",
            "win": "Windows",
        }
        target_arch_to_go_arch = {
            "amd64": "x86_64",
            "aarch64": "arm64",
        }
        file_path = self.temp_dir / f"{self.BIN_NAME}_{target_os_info}_{target_arch}.tar.gz"
        request.urlretrieve(
            self.YAMLFMT_REPO.format(
                version=re.sub(r"[ab]\d+$", "", self.metadata.version),  # 去掉版本号中的后缀, alpha/beta
                target_os_info=target_os_info_to_go_os.get(target_os_info, target_os_info),
                target_arch=target_arch_to_go_arch.get(target_arch, target_arch),
            ),
            file_path,
        )
        return file_path

    def finalize(self, version, build_data, artifact_path):
        # 清理临时目录
        shutil.rmtree(self.temp_dir)
        super().finalize(version, build_data, artifact_path)
