#!/usr/bin/env python3
"""
Test suite for yamlfmt functionality across different platforms.
"""

from __future__ import annotations

import platform
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestYamlfmtOutput(unittest.TestCase):
    """Test yamlfmt output across different platforms."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_yaml_content = """
# Test YAML file
name: test
version: 1.0.0
dependencies:
  - package1
  - package2
config:
    setting1: value1
    setting2:    value2
list:
- item1
-  item2
-   item3
"""

    def test_platform_detection(self):
        """Test that we can detect the current platform."""
        current_platform = platform.system()
        self.assertIn(current_platform, ["Linux", "Darwin", "Windows"])

    def test_yamlfmt_version(self):
        """Test that yamlfmt can output version information."""
        # 测试版本输出
        result = subprocess.run(
            [sys.executable, "-m", "yamlfmt", "-version"], capture_output=True, text=True, timeout=30, check=False
        )
        # yamlfmt 可能使用不同的版本标志，我们测试几种可能性
        if result.returncode != 0:
            result = subprocess.run(
                [sys.executable, "-m", "yamlfmt", "--version"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        if result.returncode != 0:
            result = subprocess.run(
                [sys.executable, "-m", "yamlfmt", "-h"], capture_output=True, text=True, timeout=30, check=False
            )

        assert result.returncode == 0, f"yamlfmt failed with exit code {result.returncode}"

    def test_yamlfmt_format_basic(self):
        """Test basic YAML formatting functionality."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(self.test_yaml_content)
            temp_file = Path(f.name)

        try:
            # 尝试格式化文件
            result = subprocess.run(
                [sys.executable, "-m", "yamlfmt", str(temp_file)],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            assert result.returncode == 0, f"yamlfmt failed with exit code {result.returncode}"

            assert result.stderr == "", "No output from yamlfmt"

            # 检查格式化后的文件
            assert temp_file.is_file(), f"Temporary file {temp_file} does not exist after formatting"

        finally:
            # 清理临时文件
            if temp_file.exists():
                temp_file.unlink()

    def test_help_output(self):
        """Test that yamlfmt can show help information."""
        result = subprocess.run(
            [sys.executable, "-m", "yamlfmt", "-h"], capture_output=True, text=True, timeout=30, check=False
        )

        assert result.returncode == 0, f"yamlfmt help command failed with exit code {result.returncode}"

        assert "yamlfmt is a simple command line tool for formatting yaml files." in result.stdout, (
            "Help output does not contain usage information"
        )

    def test_module_import(self):
        """Test that the yamlfmt module can be imported correctly."""
        # 添加 src 目录到 Python 路径
        # 获取项目根目录并添加 src 到路径
        test_dir = Path(__file__).parent
        src_dir = test_dir.parent / "src"
        if src_dir.exists() and str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))

        from yamlfmt import BIN_NAME, __version__

        assert BIN_NAME == "yamlfmt", f"Expected BIN_NAME to be 'yamlfmt', got {BIN_NAME}"
        assert __version__, "Expected yamlfmt version to be set"

    def test_system_info(self):
        """Display system information for debugging."""
        info = {
            "Platform": platform.system(),
            "Platform Release": platform.release(),
            "Platform Version": platform.version(),
            "Architecture": platform.machine(),
            "Processor": platform.processor(),
            "Python Version": sys.version,
            "Python Executable": sys.executable,
        }

        print("\n" + "=" * 50)
        print("SYSTEM INFORMATION")
        print("=" * 50)
        for key, value in info.items():
            print(f"{key:20}: {value}")
        print("=" * 50)


if __name__ == "__main__":
    unittest.main()
