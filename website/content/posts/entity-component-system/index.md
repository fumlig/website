---
title: Implementing a Data-Oriented Entity-Component-System
created: 2019-09-27 12:00:00
groups:
  - posts
draft: true
description: |
    A brief introduction to the entity-component-system pattern (ECS) and some
    different approaches to implementing it in a data-oriented manner.

tags:
  - ecs
  - c++
---

[TOC]

## Introduction

### What is ECS

ECS is a software design pattern which follows the *composition over
inheritance* principle. This means that polymorphic behaviour should be
achieved with composition (entity x *has* y) as opposed to inheritance (entity
x *is* y).[^1]

Consider the following example making use of inheritance (in C++):

```cpp
class entity
{
    
}
```

[^1]:
    Wikipedia contributors. (2019, August 19). Composition over inheritance. In
    *Wikipedia, The Free Encyclopedia*. Retrieved 11:20, September 27, 2019, 
    from [https://en.wikipedia.org/w/index.php?title=Composition_over_inheritance&oldid=911539972](https://en.wikipedia.org/w/index.php?title=Composition_over_inheritance&oldid=911539972)
