#!/usr/bin/env python3
"""
merge_all_txt.py
自动从当前目录及所有子文件夹中搜索 .txt 文件并合并为一个文件。
"""

import os

def merge_txt_files(output_file="merged.txt", encoding="utf-8", dedupe=False):
    """
    自动搜索当前目录下所有 .txt 文件并合并到一个文件中。
    :param output_file: 输出文件名
    :param encoding: 文件编码
    :param dedupe: 是否去重（True 时会使用 set，占内存）
    """
    all_txt_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.lower().endswith(".txt"):
                all_txt_files.append(os.path.join(root, file))

    if not all_txt_files:
        print("❌ 没有找到任何 .txt 文件。")
        return

    print(f"🔍 共找到 {len(all_txt_files)} 个 .txt 文件，将合并为：{output_file}")

    seen = set() if dedupe else None
    total_lines = 0
    skipped = 0

    with open(output_file, "w", encoding=encoding, errors="ignore") as fout:
        for idx, file_path in enumerate(all_txt_files, start=1):
            print(f"[{idx}/{len(all_txt_files)}] 正在处理：{file_path}")
            try:
                with open(file_path, "r", encoding=encoding, errors="ignore") as fin:
                    for line in fin:
                        line = line.rstrip("\r\n")
                        if not line.strip():
                            continue
                        if dedupe:
                            if line in seen:
                                skipped += 1
                                continue
                            seen.add(line)
                        fout.write(line + "\n")
                        total_lines += 1
            except Exception as e:
                print(f"⚠️ 读取文件出错：{file_path} ({e})")

    print("✅ 合并完成！")
    print(f"📄 共写入 {total_lines} 行", end="")
    if dedupe:
        print(f"，跳过重复 {skipped} 行。")
    else:
        print("。")

if __name__ == "__main__":
    # 修改参数也可以从命令行改写
    merge_txt_files(output_file="merged.txt", dedupe=True)
