#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import os.path
import click
import tinify

tinify.key = "CbQM3GiRp3t1vhOJc-9MayUXNfcA0wil"  # API KEY
version = "1.0.1"  # 版本


# 压缩的核心
def compress_core(inputFile, outputFile, img_width):
    source = tinify.from_file(inputFile)


    if img_width is not -1:
        resized = source.resize(method="scale", width=img_width)
        resized.to_file(outputFile)
    else:
        print "压缩成功:" + inputFile
        source.to_file(outputFile)


# 压缩一个文件夹下的图片
def compress_path(path, width):
    print "compress_path-------------------------------------"
    if not os.path.isdir(path):
        print "这不是一个文件夹，请输入文件夹的正确路径!"
        #compress_path(path, width)  # 压缩当前目录下的文件
        return
    else:
        fromFilePath = path  # 源路径
        toFilePath = path + "/tiny"  # 输出路径
        print "fromFilePath=%s" % fromFilePath
        print "toFilePath=%s" % toFilePath

        for root, dirs, files in os.walk(fromFilePath):
            print "root = %s" % root
            print "dirs = %s" % dirs
            print "files= %s" % files
            # for dir in dirs:
            for name in files:
                fileName, fileSuffix = os.path.splitext(name)
                if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
                    toFullPath = toFilePath + root[len(fromFilePath):]
                    toFullName = toFullPath + '/' + name
                    if os.path.isdir(toFullPath):
                        compress_path(root + '/' + name, width)
                    else:
                        os.mkdir(toFullPath)
                        compress_core(root + '/' + name, toFullName, width)
                else:
                    compress_path(root + '/' + name, width)
            break  # 仅遍历当前目录


def dirlist(path, allfile):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            fileName, fileSuffix = os.path.splitext(filepath)
            if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':

                theFileSize = os.path.getsize(filepath)
                sizekb = theFileSize/1024
                if sizekb > 200:
                    print(filepath +" size = %dkb" %(sizekb));
                    allfile.append(filepath)
                    compress_core(filepath, filepath, -1)


    # print("图片总数为:%d"%(i))
    return allfile



 # 仅压缩指定文件
def compress_file(inputFile, width):
    print "compress_file-------------------------------------"
    if not os.path.isfile(inputFile):
        print "进入下一个文件夹!"
        compress_path(inputFile, width)  # 压缩当前目录下的文件
        return
    print "file = %s" % inputFile
    dirname = os.path.dirname(inputFile)
    basename = os.path.basename(inputFile)
    fileName, fileSuffix = os.path.splitext(basename)
    if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
        compress_core(inputFile, dirname + "/tiny_" + basename, width)
    else:
        print "不支持该文件类型!"


@click.command()
@click.option('-f', "--file", type=str, default=None, help="单个文件压缩")
@click.option('-d', "--dir", type=str, default=None, help="被压缩的文件夹")
@click.option('-w', "--width", type=int, default=-1, help="图片宽度，默认不变")
def run(file, dir, width):

    # dirlist
    filelist = dirlist(os.getcwd()+"/test3", [])
    print("压缩总数%d" %(len(filelist)))



    # print ("GcsSloop TinyPng V%s" % (version))
    # if file is not None:
    #     compress_file(file, width)  # 仅压缩一个文件
    #     pass
    # elif dir is not None:
    #     compress_path(dir, width)  # 压缩指定目录下的文件
    #     pass
    # else:
    #     compress_path(os.getcwd()+"/test2", width)  # 压缩当前目录下的文件
    # print "结束!"


if __name__ == "__main__":
    run()
