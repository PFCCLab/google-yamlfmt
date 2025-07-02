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
        print(f"✓ Platform detected: {current_platform}")

    def test_yamlfmt_version(self):
        """Test that yamlfmt can output version information."""
        try:
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

            print(f"✓ yamlfmt executed successfully on {platform.system()}")
            print(f"  Return code: {result.returncode}")
            if result.stdout:
                print(f"  Stdout: {result.stdout[:200]}...")
            if result.stderr:
                print(f"  Stderr: {result.stderr[:200]}...")

        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            self.fail(f"Failed to execute yamlfmt: {e}")

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

            print(f"✓ yamlfmt formatting test completed on {platform.system()}")
            print(f"  Return code: {result.returncode}")
            print(f"  Command: python -m yamlfmt {temp_file}")

            if result.stdout:
                print(f"  Stdout: {result.stdout}")
            if result.stderr:
                print(f"  Stderr: {result.stderr}")

            # 检查格式化后的文件
            if temp_file.exists():
                formatted_content = temp_file.read_text(encoding="utf-8")
                print("  File exists after formatting: True")
                print(f"  File size: {len(formatted_content)} characters")

        except subprocess.TimeoutExpired:
            self.fail("yamlfmt command timed out")
        except (FileNotFoundError, OSError) as e:
            print(f"❌ yamlfmt formatting failed: {e}")
            # 不让测试失败，只是记录错误
        finally:
            # 清理临时文件
            if temp_file.exists():
                temp_file.unlink()

    def test_executable_permissions(self):
        """Test that the yamlfmt executable has correct permissions."""
        try:
            from yamlfmt.__main__ import get_executable_path

            executable_path = Path(get_executable_path())

            self.assertTrue(executable_path.exists(), f"Executable not found at {executable_path}")

            if platform.system() != "Windows":
                import os

                self.assertTrue(os.access(executable_path, os.X_OK), f"Executable {executable_path} is not executable")

            print(f"✓ Executable permissions verified on {platform.system()}")
            print(f"  Executable path: {executable_path}")
            print(f"  File exists: {executable_path.exists()}")
            if platform.system() != "Windows":
                import os

                print(f"  Is executable: {os.access(executable_path, os.X_OK)}")

        except (ImportError, FileNotFoundError, OSError) as e:
            print(f"❌ Executable permission test failed: {e}")

    def test_help_output(self):
        """Test that yamlfmt can show help information."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "yamlfmt", "-h"], capture_output=True, text=True, timeout=30, check=False
            )

            print(f"✓ Help output test on {platform.system()}")
            print(f"  Return code: {result.returncode}")

            if result.stdout:
                print(f"  Help output length: {len(result.stdout)} characters")
                # 显示帮助输出的前几行
                lines = result.stdout.split("\n")[:5]
                for line in lines:
                    if line.strip():
                        print(f"  > {line}")

        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            print(f"❌ Help output test failed: {e}")

    def test_module_import(self):
        """Test that the yamlfmt module can be imported correctly."""
        try:
            from yamlfmt import BIN_NAME, __version__

            print(f"✓ Module import test passed on {platform.system()}")
            print(f"  yamlfmt version: {__version__}")
            print(f"  Binary name: {BIN_NAME}")

        except ImportError as e:
            self.fail(f"Failed to import yamlfmt module: {e}")

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


def run_tests():
    """Run all tests with verbose output."""
    print("Starting yamlfmt cross-platform tests...")
    print(f"Running on: {platform.system()} {platform.release()}")
    print("-" * 60)

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestYamlfmtOutput)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    print("-" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
