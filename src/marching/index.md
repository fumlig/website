---
title: Marching Cubes
lang: en
abstract: |
  Polygonising a Scalar Field.
keywords:
- C
- C++
- marching cubes
- computer graphics
bibliography: references.bib
...

Marching cubes [@lorensen1987marching].

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

```c
void march(float* rho, struct mesh* mesh)
{
    
}
```