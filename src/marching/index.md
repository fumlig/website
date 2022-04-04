---
title: Isosurfaces with Marching Cubes
lang: en
date: 2022-03-27
abstract: |
  Polygonising a Scalar Field.
keywords:
- C
- C++
- marching cubes
- computer graphics
bibliography: references.bib
toc: true
...

Marching cubes [@lorensen1987marching].

- https://en.wikipedia.org/wiki/Isosurface
- https://en.wikipedia.org/wiki/Implicit_surface

- https://developer.nvidia.com/gpugems/gpugems3/part-i-geometry/chapter-1-generating-complex-procedural-terrains-using-gpu




- https://en.wikipedia.org/wiki/Function_representation

## Structure Definitions

```c
struct vec3
{
    float x;
    float y;
    float z;
};

struct vertex
{
    vec3 position;
    vec3 normal;
};

struct mesh
{
    struct vertex* vertices;
    unsigned* indices;
};
```

This is the function we want to implement.
Given a 

```c
void march(float* w, struct mesh* mesh)
{

}
```