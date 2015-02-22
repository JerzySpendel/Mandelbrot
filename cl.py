__author__ = 'jerzy'
import pyopencl as cl
import numpy as np
import time
from PIL import Image, ImageDraw
import sys
size = 4000
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

a_np = np.dstack(np.meshgrid(np.linspace(-2, 2, size), np.linspace(-2, 2, size))).reshape(-1, 2).astype(np.float32)
a_np = np.hstack((a_np, np.zeros((a_np.shape[0], 2)))).astype(np.float32)
a_g = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, size=a_np.nbytes)
cl.enqueue_write_buffer(queue, a_g, a_np)
kernel = """
    struct Complex{
        float x; float y;
    };
    struct Complex square_c(const struct Complex c){
        struct Complex c1; c1.x = c.x*c.x-c.y*c.y;
        c1.y = 2*c.x*c.y;
        return c1;
    }
    struct Complex sum_c(const struct Complex c1, const struct Complex c2){
        struct Complex c; c.x = c1.x+c2.x; c.y = c1.y+c2.y;
        return c;
    }
    int check_julia_point(const struct Complex p){
        struct Complex c; c.x = -0.1; c.y = 0.65;
        struct Complex z; z.x = p.x; z.y = p.y;
        int i;
        for(i = 0; i < 50; i++){
            z = sum_c(square_c(z), c);
            if (z.x*z.x + z.y*z.y > 4.0){
                return 0;
            }
        }
        return 1;
    }
    int check_mandelbrot_point(const struct Complex c){
        struct Complex z; z.x = 0; z.y = 0;
        int i;
        for(i = 0; i < 50; i++){
            z = sum_c(square_c(z), c);
            if( z.x*z.x + z.y*z.y > 4.0){
                return 0;
            }
        }
        return 1;
    }
    __kernel void calc(__global float4 *a_g){
        const int gid = get_global_id(0);
        struct Complex c;
        c.x = a_g[gid].x;
        c.y = a_g[gid].y;
        if( check_julia_point(c) == 1){
            a_g[gid].z = 1;
        }
        else{
            a_g[gid].z = 0;
        }
    }
    """
prog = cl.Program(ctx, kernel).build()
prog.calc(queue, a_np.shape, None, a_g)
res_np = np.empty_like(a_np)
cl.enqueue_read_buffer(queue, a_g, res_np).wait()
