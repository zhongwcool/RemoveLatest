import os
import re
import msvcrt
from pathlib import Path
from typing import Optional, Tuple


def read_work_directory() -> str:
    """从 removelatest.txt 中读取工作目录"""
    with open('removelatest.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('source='):
                return line.split('=', 1)[1].strip()
    raise ValueError("未找到工作目录配置（source=）")


def parse_version(filename: str) -> Optional[Tuple[int, int, int, int]]:
    """从文件名中解析版本号，返回 (年, 主版本, 次版本, 构建号) 或 None
    
    支持格式：
    - xxx_2025.1.3.exe -> (2025, 1, 3, 0)
    - xxx_2025.1.3.1230.exe -> (2025, 1, 3, 1230)
    """
    # 先尝试匹配4段版本号：xxx_2025.1.3.1230.exe
    pattern_4 = r'_(\d{4})\.(\d+)\.(\d+)\.(\d+)\.exe$'
    match = re.search(pattern_4, filename)
    if match:
        year = int(match.group(1))
        major = int(match.group(2))
        minor = int(match.group(3))
        build = int(match.group(4))
        return (year, major, minor, build)
    
    # 再尝试匹配3段版本号：xxx_2025.1.3.exe，将构建号视为0
    pattern_3 = r'_(\d{4})\.(\d+)\.(\d+)\.exe$'
    match = re.search(pattern_3, filename)
    if match:
        year = int(match.group(1))
        major = int(match.group(2))
        minor = int(match.group(3))
        build = 0  # 3段版本号时，构建号默认为0
        return (year, major, minor, build)
    
    return None


def find_latest_version_file(directory: Path) -> Optional[Path]:
    """在目录中找出版本号最新的文件"""
    latest_file = None
    latest_version = None
    
    if not directory.exists() or not directory.is_dir():
        return None
    
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix == '.exe':
            version = parse_version(file_path.name)
            if version:
                if latest_version is None or version > latest_version:
                    latest_version = version
                    latest_file = file_path
    
    return latest_file


def get_file_size_mb(file_path: Path) -> float:
    """获取文件大小（MB）"""
    size_bytes = file_path.stat().st_size
    return size_bytes / (1024 * 1024)


def wait_for_key() -> str:
    """等待用户按键，返回 'enter' 或 'esc'"""
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            # 回车键
            if key == b'\r' or key == b'\n':
                return 'enter'
            # ESC键
            elif key == b'\x1b':
                return 'esc'
            # 其他键忽略，继续等待


def main():
    try:
        # 读取工作目录
        work_dir = read_work_directory()
        work_path = Path(work_dir)
        
        if not work_path.exists():
            print(f"错误：工作目录不存在: {work_dir}")
            return
        
        print(f"工作目录: {work_dir}\n")
        
        # 遍历所有子目录（渠道）
        channels = [d for d in work_path.iterdir() if d.is_dir()]
        
        if not channels:
            print("未找到任何渠道子目录")
            return
        
        # 为每个渠道找出版本号最新的文件
        latest_files = []
        for channel_dir in channels:
            latest_file = find_latest_version_file(channel_dir)
            if latest_file:
                latest_files.append((channel_dir.name, latest_file))
        
        if not latest_files:
            print("未找到任何版本文件")
            return
        
        # 询问是否删除每个最新版本文件
        print("找到以下最新版本文件：\n")
        for channel, file_path in latest_files:
            version = parse_version(file_path.name)
            size_mb = get_file_size_mb(file_path)
            print(f"渠道: {channel}")
            print(f"文件: {file_path.name}")
            # 显示版本号，如果是构建号为0则只显示3段
            if version[3] == 0:
                print(f"版本: {version[0]}.{version[1]}.{version[2]}")
            else:
                print(f"版本: {version[0]}.{version[1]}.{version[2]}.{version[3]}")
            print(f"大小: {size_mb:.2f} MB")
            print(f"路径: {file_path}")
            print("\n是否删除？[回车=删除, ESC=跳过]")
            
            key = wait_for_key()
            
            if key == 'enter':
                try:
                    file_path.unlink()
                    print(f"✓ 已删除: {file_path.name}\n")
                except Exception as e:
                    print(f"✗ 删除失败: {e}\n")
            else:
                print(f"⊘ 已跳过: {file_path.name}\n")
        
        print("处理完成！")
        
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
