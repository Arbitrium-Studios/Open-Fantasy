import os
import platform
import subprocess
import sys

# Astron Variable Location of Astron for Win32
astron_win32 = os.getcwd() + "/astrond_win32.exe"
astron_win32 = astron_win32.replace("\\", "/")

# Astron Variable Location of Astron for Linux
astron_linux = os.getcwd() + "/astrond_linux"

# Astron Variable Location of Astron for macOS on Intel
astron_darwin = os.getcwd() + "/astrond_darwin"

# Astron Variable Location of Astron for macOS on Apple Silicon
astron_darwin_arm = os.getcwd() + "/astrond_darwin_arm"

# Arguments for Astron for Win32
args_win32 = os.getcwd() + "/config/cluster.yml"
args_win32 = args_win32.replace("\\", "/")

# Arguments for Astron for Platforms other then Win32
args_other = os.getcwd() + "/config/cluster.yml"

#Check if OS is not "Windows" and if so assign variable "args" to "args_other"
if platform.system() != "Windows":
    args = args_other

#Check if OS is "Windows" and if so assign variable "args" to "args_win32" and "astron" to "astron_win32"
if platform.system() == "Windows":
    args = args_win32
    astron = astron_win32

#Check if OS is "Linux" and if so assign variable "astron" to "astron_linux"
if platform.system() == "Linux":
    astron = astron_linux

#Check if OS is "Darwin" and further check if architecture is "arm64" if so assign variable "astron" to "astron_darwin_arm"
if platform.system() == "Darwin" and platform.machine() == "arm64":
    astron = astron_darwin_arm

#Check if OS is "Darwin" and further check if architecture is "x86_64" if so assign variable "astron" to "astron_darwin"
if platform.system() == "Darwin" and platform.machine() == "x86_64":
    astron = astron_darwin

subprocess.run([astron, "-p", "--loglevel", "info", args])