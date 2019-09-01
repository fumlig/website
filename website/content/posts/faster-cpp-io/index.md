---
title: Faster C++ I/O
created: 2019-08-28 17:00:00
groups:
  - posts
draft: false
description: Some tricks for faster C++ input and output.

tags:
  - c
  - c++
  - competitive programming
---

[TOC]

## Different I/O Alternatives

### std::cin and std::cout

Using `<iostream>`´s `std::cin` and `std::cout` is the preferred way to handle
input and output in C++. It's type-safe and extensible, but all of this comes
at a cost. Let's look at an example program.

```cpp
{!posts/faster-cpp-io/iostream.cpp!}
```

Compiling this program with g++ version 9.10 and 1 000 000 randomized integers
between -10 000 and 10 000 as input takes 0,539 seconds.

I/O Alternative                                      | Time (s)
---------------------------------------------------- | --------
`std::cin` and `std::cout`                           | 0,539

This doesn't seem half bad but we can do better!

#### Disable Synchronization

The C and C++ standard streams are per default synchronized. This allows you to
mix C- and C++-style I/O and get deterministic results. However, if you are
sure that you won't use C-style I/O, you can disable this synchronization. This
can lead to an improvement in performance.

To disable synchronization, add following line to your program:

```cpp hl_lines="5"
{!posts/faster-cpp-io/iostream-nosync.cpp!}
```

This brings the program runtime down to 0,421 seconds.

I/O Alternative                                      | Time (s)
---------------------------------------------------- | --------
`std::cin` and `std::cout`, synchronization disabled | 0,421
`std::cin` and `std::cout`                           | 0,539

#### Untying `std::cin` from `std::cout`

One additional trick is to untie `std::cin` from `std::cout`. Tied streams
ensure that one stream is flushed before any I/O operations on the other.
It is possible to untie the two streams with the following function call:

```cpp hl_lines="6"
{!posts/faster-cpp-io/iostream-notie.cpp!}
```

Running this program takes 0,100 seconds, which is a massive improvement.

I/O Alternative                                      | Time (s)
---------------------------------------------------- | --------
`std::cin` and `std::cout`, untied                   | 0,100
`std::cin` and `std::cout`, synchronization disabled | 0,421
`std::cin` and `std::cout`                           | 0,539

### scanf() and printf()

The C standard library provides the `scanf()` and
`printf()` functions. These are more primitive and less
safe than C++'s `std::cin` and `std::cout` but usually quite a lot faster.

```c
{!posts/faster-cpp-io/stdio.c!}
```

Compiled with gcc version 9.10 and ran with the same input as previous
programs, this takes 0,141 seconds.

I/O Alternative                                      | Time (s)
---------------------------------------------------- | --------
`std::cin` and `std::cout`, untied                   | 0,100
`scanf()` and `printf()`                             | 0,141
`std::cin` and `std::cout`, synchronization disabled | 0,421
`std::cin` and `std::cout`                           | 0,539

So, are `std::cin` and `std::cout` unsynchronized and untied still the winners?
No - we can do better!

### getchar() and putchar()

`getchar()` and `putchar()` are the most primitive I/O functions in the C
standard library. They are used to get and put individual characters from and
to `stdin` and `stdout`.

We can take advantage of these to write our own even faster I/O functions:

```c
{!posts/faster-cpp-io/getchar-putchar.c!}
```

How long does this take to run? 0,074 seconds.

I/O Alternative                                      | Time (s)
---------------------------------------------------- | --------
`getchar()` and `putchar()`                          | 0,074
`std::cin` and `std::cout`, untied                   | 0,100
`scanf()` and `printf()`                             | 0,141
`std::cin` and `std::cout`, synchronization disabled | 0,421
`std::cin` and `std::cout`                           | 0,539

#### Unlocked

As it happens, there is one more trick we can use. Both `getchar()` and
`putchar()` are thread safe which is generally preferrable. If one really wants
the fastest possible I/O there are so called unlocked versions of `getchar()`
and `putchar()`.

On POSIX systems, these are defined as `getchar_unlocked()` and
`putchar_unlocked()`. On Windows systems, they are defined as
`_getchar_nolock()` and `_putchar_nolock()`. Let's use these in our custom I/O
functions.

```c
{!posts/faster-cpp-io/getchar-putchar-unlocked.c!}
```

This new program takes 0,055 seconds which makes it the fastest yet.

I/O Alternative                                      | Time (s)
---------------------------------------------------- | --------
`getchar()` and `putchar()`, unlocked                | 0,055
`getchar()` and `putchar()`                          | 0,074
`std::cin` and `std::cout`, untied                   | 0,100
`scanf()` and `printf()`                             | 0,141
`std::cin` and `std::cout`, synchronization disabled | 0,421
`std::cin` and `std::cout`                           | 0,539

## Conclusion

So, how should you do I/O? Usually, just use `std::cout` and `std::cin` or
`scanf()` and `printf()` as they are safe and easy to use. If you need to
squeeze out performance you can, in very specific cases use the tricks
mentioned in this article.
