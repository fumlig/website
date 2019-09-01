#!/usr/bin/env bash

g++ -o iostream iostream.cpp
g++ -o iostream-nosync iostream-nosync.cpp
g++ -o iostream-notie iostream-notie.cpp
gcc -o stdio stdio.c
gcc -o getchar-putchar getchar-putchar.c
gcc -o getchar-putchar-unlocked getchar-putchar-unlocked.c

echo "iostream"
time cat in.txt | ./iostream > /dev/null
echo "iostream-nosync"
time cat in.txt | ./iostream-nosync > /dev/null
echo "iostream-notie"
time cat in.txt | ./iostream-notie > /dev/null
echo "stdio"
time cat in.txt | ./stdio > /dev/null
echo "getchar-putchar"
time cat in.txt | ./getchar-putchar > /dev/null
echo "getchar-putchar-unlocked"
time cat in.txt | ./getchar-putchar-unlocked > /dev/null