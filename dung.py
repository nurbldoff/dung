#from __future__ import division

SCREEN_SIZE = (800, 480)

from math import radians

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
from OpenGL.GL.shaders import *

import pygame
from pygame.locals import *

from gameobjects.matrix44 import *
from gameobjects.vector3 import *

from math import *
from ctypes import *

def resize(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(100.0, float(width)/height, .1, 10.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    fogColor=(0., 0., 0., 1.0)
    #glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    #LoadTextures()
    glEnable(GL_TEXTURE_2D)

    glEnable(GL_DEPTH_TEST)
    #glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
    #glShadeModel(GL_FLAT)
    glShadeModel(GL_SMOOTH)
    #glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 50)
    glLight(GL_LIGHT0, GL_AMBIENT, (0.1,0.1,0.1,1))
    glClearColor(0.0, 0.0, 0.0, 0.0)   # background color

    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    #glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))

    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing

    glEnable(GL_FOG)                         # Enable fog
    glFogi(GL_FOG_MODE, GL_LINEAR)           # Set fog settings
    glFogfv(GL_FOG_COLOR, fogColor);         # Set fog color
    glFogf(GL_FOG_DENSITY, 0.35);            # Set fog density
    glHint(GL_FOG_HINT, GL_DONT_CARE);       # Set Hint
    glFogf(GL_FOG_START, 0.0);               # Fog start
    glFogf(GL_FOG_END, 5.5);                 # Fog end

    # glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    # glLightModeli( GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR )
    #glPolygonMode(GL_BACK,GL_FILL)
    #glPolygonMode(GL_FRONT,GL_LINE)


def LoadTextures():
    #global texture
    image = pygame.image.load("tex/cube.png")

    ix = image.get_width()
    iy = image.get_height()
    image = pygame.image.tostring(image, "RGBX", False)

    # Create Texture
    wall_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, wall_texture)   # 2d texture (x and y size)

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);

    return wall_texture

class Cube(object):


    def __init__(self, position, color, wall_tex, draw_sides = (0,1,2,3,4,5)):

        self.position = position
        self.color = color
        self.wall_texture = wall_tex
        self.draw_sides = draw_sides

    num_faces = 6

    vertices = [ (0.0, 0.0, 1.0),
                 (1.0, 0.0, 1.0),
                 (1.0, 1.0, 1.0),
                 (0.0, 1.0, 1.0),
                 (0.0, 0.0, 0.0),
                 (1.0, 0.0, 0.0),
                 (1.0, 1.0, 0.0),
                 (0.0, 1.0, 0.0) ]

    normals = [ (0.0, 0.0, 1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0) ] # bottom

    vertex_indices = [ (0, 1, 2, 3),  # front
                       (5, 4, 7, 6),  # back
                       (1, 5, 6, 2),  # right
                       (4, 0, 3, 7),  # left
                       (3, 2, 6, 7),  # top
                       (0, 4, 5, 1) ] # bottom

    texture_corners = [  (0,1), (1,1), (1,0), (0,0)]

    def render(self, program):

        #glColor( *self.color )

        # Adjust all the vertices so that the cube is at self.position
        vertices = [tuple(Vector3(v) + self.position) for v in self.vertices]
        glEnable(GL_DEPTH_TEST)
        # Draw all 6 faces of the cube
        glBegin(GL_QUADS)
        for face_no in self.draw_sides:
            glBindTexture(GL_TEXTURE_2D, self.wall_texture)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            #glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
            #glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
            n_tex = 4.
            if face_no in (0,1,2,3):
                tex_offset = 0.
            else:
                tex_offset = 3.

            subdivisions = 1
            tex_corns = [((c[0]+tex_offset)/n_tex/subdivisions, c[1]/float(subdivisions)) for c in self.texture_corners]

            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glNormal3dv( self.normals[face_no] )

            # # IDK why this doesn't work...
            # vs = map(Vector3, [vertices[x] for x in (v1, v2, v3, v4)])
            # faceCenter_location = glGetAttribLocation(program, "faceCenter")
            # print "location:", faceCenter_location
            # vCenter = (vs[0]+vs[1]+vs[2]+vs[3])/4
            # glEnableVertexAttribArray( faceCenter_location )
            # glVertexAttribPointer(
            #         faceCenter_location,
            #         3, GL_FLOAT,False, stride, vCenter.as_tuple()
            #     )
            # glVertexAttrib3f(faceCenter_location, GLfloat(vCenter.x), GLfloat(vCenter.y), GLfloat(vCenter.z))
            for subface_x in range(subdivisions):
                for subface_y in range(subdivisions):

                    glTexCoord2f(tex_corns[0][0], tex_corns[0][1])
                    glVertex( vertices[v1] )

                    glTexCoord2f(tex_corns[1][0], tex_corns[1][1])
                    glVertex( vertices[v2] )

                    glTexCoord2f(tex_corns[2][0], tex_corns[2][1])
                    glVertex( vertices[v3] )

                    glTexCoord2f(tex_corns[3][0], tex_corns[3][1])
                    glVertex( vertices[v4] )

        glEnd()


class Map(object):

    def __init__(self):

        self.map_surface1 = pygame.image.load("maps/map2.png")
        map_surface2 = pygame.image.load("maps/map3.png")
        self.map_surface1.lock()
        map_surface2.lock()

        w, h = self.map_surface1.get_size()

        self.cubes = []
        wall_tex = LoadTextures()

        # Create a cube for every non-white pixel
        #ceiling
        for y in range(h):
            for x in range(w):

                r, g, b, a = map_surface2.get_at((x, y))

                if (r, g, b) != (255, 255, 255):

                    gl_col = (r/255.0, g/255.0, b/255.0)
                    position = (float(x), 2.0, float(y))
                    cube = Cube( position, gl_col, wall_tex, (5,))
                    self.cubes.append(cube)

        #floor
        for y in range(h):
            for x in range(w):

                r, g, b, a = map_surface2.get_at((y, x))

                if (r, g, b) != (255, 255, 255):

                    gl_col = (r/255.0, g/255.0, b/255.0)
                    position = (float(x), -1.0, float(y))
                    cube = Cube( position, gl_col, wall_tex, (4,) )
                    self.cubes.append(cube)
        # walls
        for y in range(h):
            for x in range(w):

                r, g, b, a = self.map_surface1.get_at((x, y))


                if (r, g, b) != (255, 255, 255):
                    neighbors = []
                    for i, coord in enumerate( ((x, y+1), (x, y-1), (x+1, y), (x-1, y)) ):
                        try:
                            n = self.map_surface1.get_at(coord)
                            if n == (255,255,255,255):
                                neighbors.append(i)
                        except IndexError:
                            pass

                    gl_col = (r/255.0, g/255.0, b/255.0)
                    position = (float(x), 0.0, float(y))
                    cube = Cube( position, gl_col, wall_tex, neighbors)
                    self.cubes.append(cube)
                    position = (float(x), 1.0, float(y))
                    cube = Cube( position, gl_col, wall_tex, neighbors)
                    self.cubes.append(cube)


        self.map_surface1.unlock()
        map_surface2.unlock()

        self.display_list = None

    def is_wall(self, pos):
        r, g, b, a = self.map_surface1.get_at((int(pos[0]), int(pos[2])))
        return (r,g,b) != (255,255,255)

    def render(self, program):

        if self.display_list is None:
            print "remaking map..."
            # Create a display list
            self.display_list = glGenLists(1)
            glNewList(self.display_list, GL_COMPILE)

            # Draw the cubes
            for cube in self.cubes:
                cube.render(program)

            # End the display list
            glEndList()

        else:

            # Render the display list
            glCallList(self.display_list)


class Player(object):

    direction_map = map(Vector3,
                     ((0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 0,-1),
                      (0, 0 ,-1), (-1, 0,-1), (-1, 0, 0), (-1, 0, 1)))

    def __init__(self, level, start_position, start_direction):
        self.map = level
        self.position = start_position    # a 3-vector with integers
        self.direction = start_direction  # an integer 0..7, 0 is along global z-axis

    def move_forward(self, steps=1):
        movement = -self.direction_map[self.direction]*steps
        new_position = self.position+movement
        if not self.map.is_wall(new_position.as_tuple()):
            self.position = new_position
            return movement
        else:
            return Vector3(0,0,0)

    def move_backward(self, steps=1):
        movement = self.direction_map[self.direction]*steps
        new_position = self.position+movement
        if not self.map.is_wall(new_position.as_tuple()):
            self.position = new_position
            return movement
        else:
            return Vector3(0,0,0)

    def move_right(self, steps=1):
        movement = self.direction_map[(self.direction+2)%8]*steps
        new_position = self.position+movement
        if not self.map.is_wall(new_position.as_tuple()):
            self.position = new_position
            return movement
        else:
            return Vector3(0,0,0)

    def move_left(self, steps=1):
        movement = self.direction_map[(self.direction-2)%8]*steps
        new_position = self.position+movement
        if not self.map.is_wall(new_position.as_tuple()):
            self.position = new_position
            return movement
        else:
            return Vector3(0,0,0)

    def turn_right(self, steps=1):
        self.direction = (self.direction-steps)%8
        return -pi/4

    def turn_left(self, steps=1):
        self.direction = (self.direction+steps)%8
        return pi/4

    def get_position_delta(self):
        return self.direction_map[self.direction]

def prepare_fbo():
    #glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(110.0, 1.0, 0.1, 10.)
    glMatrixMode(GL_MODELVIEW)
    #glLoadIdentity()
    #glEnable( GL_DEPTH_TEST );
    #glEnable(GL_TEXTURE_2D)
    #time_passed = clock.tick(30)
    # time_passed_seconds = time_passed / 1000.

    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()

    ### Render to a texture
    rendertarget=glGenTextures( 1 )

    glBindTexture( GL_TEXTURE_2D, rendertarget );
    glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE );
    # glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
    #                  GL_REPEAT);
    # glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
    #                  GL_REPEAT );
    #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB ,512, 512,0,GL_RGBA,
                 GL_UNSIGNED_INT, None)

    fbo=c_uint(1) # WTF? Did not find a way to get there easier
    # A simple number would always result in a "Segmentation
    # Fault" for me
    glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER_EXT, fbo);

    depthbuffer = c_uint(2)
    glGenRenderbuffersEXT(1)
    glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, depthbuffer)
    glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT, GL_DEPTH_COMPONENT, 512, 512)
    glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT, GL_DEPTH_ATTACHMENT_EXT, GL_RENDERBUFFER_EXT, depthbuffer)

    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                           GL_TEXTURE_2D, rendertarget, 0)




    # Align viewport to Texture dimensions - Try rendering
    # to different dimensions than the texture has to find out
    # about how your hardware handles display pitch
    glPushAttrib(GL_VIEWPORT_BIT);
    glViewport(0, 0, 512, 512);

    return fbo, rendertarget, depthbuffer

def run():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

    init()
    resize(*SCREEN_SIZE)

    CAVE_VERTEX_SHADER = compileShader(
        """
        attribute vec3 faceCenter;
        vec4 a,n;
        float newx, b;
        //varying vec3 glFrontColor;
        varying float fogFactor, surfaceCosine;


        void main() {

        gl_Position = ftransform();
        vec3 vVertex = vec3(gl_ModelViewMatrix * gl_Vertex);
        n.xyz = gl_Normal;
        n[3] = 0;
        a = normalize(gl_ModelViewMatrix*n);
        surfaceCosine = dot(a.xyz, normalize(vVertex.xyz));  // cosine between viewline and normal
        if (a.y == 0) {
            if(a.x<-0.5) {
                gl_TexCoord[0].x = gl_MultiTexCoord0.x+0.25;
            } else {
                if (a.x>0.5) {
                    gl_TexCoord[0].x = gl_MultiTexCoord0.x+0.5;
                } else {
                    gl_TexCoord[0].x = gl_MultiTexCoord0.x;
                }
            }
        } else {
            gl_TexCoord[0].x = gl_MultiTexCoord0.x;
        }
        gl_TexCoord[0].y = gl_MultiTexCoord0.y;


        gl_FogFragCoord = length(vVertex);
        //gl_FronColor = gl_Color;   // * length(gl_Position) / 5.0;

        fogFactor = exp2( -gl_Fog.density *
                          gl_Fog.density *
                          gl_FogFragCoord *
                          gl_FogFragCoord
                           );
        fogFactor = clamp(fogFactor, 0.0, 1.0);
        surfaceCosine = abs(surfaceCosine);

        }

        /*
        varying float xpos;
        varying float ypos;
        varying float zpos;
        //varying vec3 glFrontColor;

        void main(void)
        {
        xpos = clamp(gl_Vertex.x,0.0,1.0);
        ypos = clamp(gl_Vertex.y,0.0,1.0);
        zpos = clamp(gl_Vertex.z,0.0,1.0);

        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

        }*/
        """,
        GL_VERTEX_SHADER)

    CAVE_FRAGMENT_SHADER = compileShader(
        """
        uniform sampler2D tex;
        varying float fogFactor, surfaceCosine;

        void main()
        {

        vec4 color = texture2D(tex,gl_TexCoord[0].st);   // normal texturing
        gl_FragColor = mix(gl_Fog.color, color, fogFactor*surfaceCosine);
        }

        /*
        varying float xpos;
        varying float ypos;
        varying float zpos;

        void main (void)
        {

        gl_FragColor = mix(gl_Fog.color, vec4 (xpos, ypos, zpos, 1.0);
        }*/
        """,
        GL_FRAGMENT_SHADER)

    cave_shader = compileProgram(CAVE_VERTEX_SHADER, CAVE_FRAGMENT_SHADER)

    VERTEX_SHADER = compileShader(
        """
        float a = .1;
        float x, y, p, p2, d;
        void main(void)
        {
        gl_TexCoord[0] = gl_MultiTexCoord0;
        x = gl_TexCoord[0][0]*2-1;
        y = gl_TexCoord[0][1]*2-1;
        p2 = (x*x + y*y);
        p = sqrt(p2);
        d = pow(p/(1.0-a*p2),2);
        gl_TexCoord[0][0] = ((x / (1-a*d))+1)*.5;
        gl_TexCoord[0][1] = ((y / (1-a*d))+1)*.5;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }
        """,
        GL_VERTEX_SHADER
        )

    FRAGMENT_SHADER = compileShader(
        """
        uniform sampler2D myTexture;
        float a = .25;
        float x, y, p, p2, d;
        void main (void)
        {
        x = gl_TexCoord[0][0]*2-1;
        y = gl_TexCoord[0][1]*2-1;
        p2 = (x*x + y*y);
        p = sqrt(p2);
        d = pow(p/(1.0-a*p2),2);
        x = ((x / (1-a*d))+1)*.5;
        y = ((y / (1-a*d))+1)*.5;
        gl_FragColor  = texture2D(myTexture, vec2(x, y));
        }

        """,
        GL_FRAGMENT_SHADER
        )
    shader = compileProgram(FRAGMENT_SHADER)
    clock = pygame.time.Clock()

    # glMaterial(GL_FRONT, GL_AMBIENT, (1.0, 0.1, 0.1, 1.0))
    # glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glCullFace(GL_BACK)
    glEnable(GL_CULL_FACE)

    # This object renders the 'map'
    level = Map()
    player = Player(level, start_position = Vector3(10, 0, 10),
                    start_direction = 0)

    # Camera transform matrix
    camera_matrix = Matrix44()
    camera_matrix.translate = (10.5, .5, 10.5)

    # Initialize speeds and directions
    rotation_direction = Vector3()
    rotation_speed = radians(90.0)
    movement_direction = Vector3()
    movement_speed = 5.0

    #player_direction_delta = Vector3()
    player_position_delta = Vector3()

    while True:

        clock.tick(100)

        for event in pygame.event.get():


            if event.type == QUIT:
                return
            elif event.type == KEYUP and event.key == K_ESCAPE:
                return
            elif event.type == pygame.KEYDOWN:

                # Reset rotation and movement direction deltas
                player_position_delta.set(0.0, 0.0, 0.0)
                player_direction_delta = 0

                rotation_direction.set(0.0, 1.0, 0.0)
                movement_direction.set(0.0, 0.0, 0.0)

                if event.key == K_w:
                    #movement_direction.z = -1.0
                    player_position_delta = player.move_forward()
                elif event.key == K_s:
                    #movement_direction.z = +1.0
                    player_position_delta = player.move_backward()
                elif event.key == K_q:
                    #movement_direction.x = -1.0
                    player_direction_delta = player.turn_left()
                elif event.key == K_e:
                    #movement_direction.x = +1.0
                    player_direction_delta = player.turn_right()
                elif event.key == K_a:
                    #rotation_direction.y = +1.0
                    player_position_delta = player.move_left()
                elif event.key == K_d:
                    #     rotation_direction.y = -1.0
                    player_position_delta = player.move_right()

                print camera_matrix
                print player.position

                time_steps = 10
                if True:
                    for i in range(10):
                        print i,
                        #init()
                        # Clear the screen, and z-buffer

                        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                        glClearColor(0.0, 0.0, 0.0, 0.0)


                        #glEnable(GL_BLEND);
                        ###glBlendFunc (GL_SRC_ALPHA, GL_ONE);

                        #glClearColor(0.0, 0.0, 0.0, 0.0)

                        # Obtain an frabebuffer object into which to render the dungeon
                        fbo, rendertarget, depthbuffer = prepare_fbo()

                        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                        glColor4f(1,1,1,1)
                        #texture=glGenTextures( 1 )


                        # Calculate rotation matrix and multiply by camera matrix
                        rotation = rotation_direction * player_direction_delta/time_steps
                        rotation_matrix = Matrix44.xyz_rotation(*rotation)
                        camera_matrix *= rotation_matrix

                        # # Calcluate movment and add it to camera matrix translate
                        # heading = Vector3(camera_matrix.forward)
                        # right = Vector3(camera_matrix.right)
                        # movement = heading *movement_direction.z + right *movement_direction.x
                        camera_matrix.translate += player_position_delta/time_steps

                        # Upload the inverse camera matrix to OpenGL
                        glLoadMatrixd(camera_matrix.get_inverse().to_opengl())


                        # # Light must be transformed as well
                        # offset = (player.position+player_position_delta/time_steps*i)
                        # glLight(GL_LIGHT0, GL_POSITION, (camera_matrix[3,0]-0,
                        #                                  camera_matrix[3,1]-0,
                        #                                  camera_matrix[3,2]-0,
                        #                                  1.))

                        glUseProgram(cave_shader)

                        #glEnable( GL_TEXTURE_2D );
                        level.render(cave_shader)
                        #glFlush()

                        # stop rendering to FBO
                        glPopAttrib()
                        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)

                        #glDisable( GL_BLEND );
                        glEnable( GL_TEXTURE_2D );


                        glClearColor(.1, 0.0, 0.0, 1.0)	# This Will Clear The Background Color To Black
                        glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer

                        glMatrixMode(GL_PROJECTION)
                        glLoadIdentity()
                        #gluPerspective(45.0, 8./6, 0.1, 100.0)

                        gluPerspective(45.0, 8.0/4.8, 0.1, 10.0)

                        glMatrixMode(GL_MODELVIEW)
                        glLoadIdentity()

                        glBindTexture( GL_TEXTURE_2D, rendertarget )

                        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
                                         GL_CLAMP);
                        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                                         GL_CLAMP);
                        gluLookAt(0, 0, 2.4,
                                  0, 0, 1,
                                  0, 1, 0)

                        # Draw a single quad to serve as view
                        glColor3f(0.9, 0.9, 1.0)            # Bluish shade
                        glUseProgram(shader)
                        glBegin(GL_QUADS)
                        glTexCoord2f(.85,.85);
                        glVertex3f(1.0, 1.0, 0.0)           # Top Right
                        glTexCoord2f(0.15,.85);
                        glVertex3f(-1.0, 1.0, 0.0)          # Top Left
                        glTexCoord2f(0.15,0.15);
                        glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
                        glTexCoord2f(0.85, 0.15);
                        glVertex3f(1.0, -1.0, 0.0)          # Bottom Right

                        glEnd()

                        glFlush()
                        glUseProgram(0)

                        # Show the screen
                        pygame.display.flip()

                        # glDisable( GL_BLEND );
                        # glEnable( GL_TEXTURE_2D );
                        # glEnable( GL_DEPTH_TEST );
                        # glDeleteTextures(texture)

                        # Free some memory
                        glDeleteFramebuffers(1, depthbuffer)
                        glDeleteTextures(rendertarget)
                        glDeleteFramebuffers(1,fbo)

run()
