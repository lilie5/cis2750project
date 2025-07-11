//Include phylib.h
#include "phylib.h"
// UTILITY FUNCTIONS
void phylib_print_object( phylib_object *object )
{
  if (object==NULL)
  {
    printf( "NULL;\n" );
    return;
  }

  switch (object->type)
  {
    case PHYLIB_STILL_BALL:
      printf( "STILL_BALL (%d,%6.1lf,%6.1lf)\n",
	      object->obj.still_ball.number,
	      object->obj.still_ball.pos.x,
	      object->obj.still_ball.pos.y );
      break;

    case PHYLIB_ROLLING_BALL:
      printf( "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)\n",
              object->obj.rolling_ball.number,
              object->obj.rolling_ball.pos.x,
              object->obj.rolling_ball.pos.y,
              object->obj.rolling_ball.vel.x,
              object->obj.rolling_ball.vel.y,
              object->obj.rolling_ball.acc.x,
              object->obj.rolling_ball.acc.y );
      break;

    case PHYLIB_HOLE:
      printf( "HOLE (%6.1lf,%6.1lf)\n",
	      object->obj.hole.pos.x,
	      object->obj.hole.pos.y );
      break;

    case PHYLIB_HCUSHION:
      printf( "HCUSHION (%6.1lf)\n",
	      object->obj.hcushion.y );
      break;

    case PHYLIB_VCUSHION:
      printf( "VCUSHION (%6.1lf)\n",
	      object->obj.vcushion.x );
      break;
  }
}

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ) {
    //new still ball!
    phylib_object * new = (phylib_object *)malloc(sizeof(phylib_object));
    if (new == NULL) {
        return NULL;
    }
    //update here
    new->type = PHYLIB_STILL_BALL;
    new->obj.still_ball.number = number;
    new->obj.still_ball.pos.x = pos->x;
    new->obj.still_ball.pos.y = pos->y;
    return new;
}

phylib_object *phylib_new_rolling_ball( unsigned char number,
                                phylib_coord *pos,
                                phylib_coord *vel,
                                phylib_coord *acc)
{
    //make a new rolling ball -> updating all coords accordingly
    phylib_object * new = (phylib_object *)malloc(sizeof(phylib_object));
    if (new == NULL) {
        return NULL;
    }
    new->type = PHYLIB_ROLLING_BALL;
    new->obj.rolling_ball.number = number;
    //pos
    new->obj.rolling_ball.pos.x = pos->x;
    new->obj.rolling_ball.pos.y = pos->y;
    //vel
    new->obj.rolling_ball.vel.x = vel->x;
    new->obj.rolling_ball.vel.y = vel->y;
    //acc
    new->obj.rolling_ball.acc.x = acc->x;
    new->obj.rolling_ball.acc.y = acc->y;
    return new;
}

phylib_object *phylib_new_hole( phylib_coord *pos ) {
    //make a new hole
    phylib_object * new = (phylib_object *)malloc(sizeof(phylib_object));
    if (new == NULL) {
        return NULL;
    }

    new->type = PHYLIB_HOLE;
    //update pos
    new->obj.hole.pos.x = pos->x;
    new->obj.hole.pos.y = pos->y;

    return new;
}

phylib_object *phylib_new_hcushion( double y ) {
    //set hcushion new
    phylib_object * new = (phylib_object *)malloc(sizeof(phylib_object));
    if (new == NULL) {
        return NULL;
    }

    new->type = PHYLIB_HCUSHION;

    new->obj.hcushion.y = y; //only y value recorded here

    return new;
}

phylib_object *phylib_new_vcushion( double x ) {
    //make a new vcushion
    phylib_object * new = (phylib_object *)malloc(sizeof(phylib_object));
    if (new == NULL) {
        return NULL;
    }

    new->type = PHYLIB_VCUSHION;

    new->obj.vcushion.x = x; //only x value recorded here

    return new;
}

phylib_table *phylib_new_table( void ) {
    //get a new table
    phylib_table * newTable = (phylib_table *)malloc(sizeof(phylib_table));
    if (newTable == NULL) {
        return NULL; //safety precaution
    }
    newTable->time = 0.0;
    //make hcushions, vcushions
    newTable->object[0] = phylib_new_hcushion(0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    newTable->object[2] = phylib_new_vcushion(0);
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    
    //balls -> use setter to update each hole accordingly
    phylib_coord setter;
    setter.x = 0.0;
    setter.y = 0.0;
    newTable->object[4] = phylib_new_hole(&setter);
    setter.y = PHYLIB_TABLE_WIDTH;
    newTable->object[5] = phylib_new_hole(&setter);
    setter.y = PHYLIB_TABLE_LENGTH;
    setter.x = 0.0;
    newTable->object[6] = phylib_new_hole(&setter);
    setter.x = PHYLIB_TABLE_WIDTH;
    setter.y = 0.0;
    //hello
    newTable->object[7] = phylib_new_hole(&setter);
    setter.x = PHYLIB_TABLE_WIDTH;
    setter.y = PHYLIB_TABLE_WIDTH;
    newTable->object[8] = phylib_new_hole(&setter);
    setter.x = PHYLIB_TABLE_WIDTH;
    setter.y = PHYLIB_TABLE_LENGTH;
    newTable->object[9] = phylib_new_hole(&setter);
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        //set the rest to null
        newTable->object[i] = NULL;
    }
    return newTable;
}

//UTILITY FUNCTIONS
void phylib_copy_object( phylib_object **dest, phylib_object **src ) {
    if (*src == NULL) {
        //printf("SRC is NULL, returning NULL\n");
        *dest = NULL;
    } else {
        *dest = (phylib_object *)malloc(sizeof(phylib_object));
        //printf("Memcpying dest and src in copy_object\n");
        memcpy(*dest, *src, sizeof(phylib_object));
    }
}

phylib_table *phylib_copy_table( phylib_table *table ) {
    phylib_table * newTable = malloc(sizeof(phylib_table));
    //printf("Created table\n");
    if (newTable == NULL) {
        //printf("newTable is NULL, returning now");
        return NULL;
    } else {
        //printf("Setting values\n");
        newTable->time = table->time;
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            //printf("Attempting copy for %d\n", i);
            //printf("COPYING: %p %p\n", (void *)newTable->object[i], (void *)table->object[i]);
            phylib_copy_object(&(newTable->object[i]),&(table->object[i]));
            //printf("PHYLIB_COPIED: %p %p\n", (void *)newTable->object[i], (void *)table->object[i]);
            /*if (table->object[i] != NULL) {
                printf("%d: %d\n", i, newTable->object[i]->type);
            }*/
            
            //newTable->object[i] = table->object[i];
        }
        //printf("Time set\n");
        //printf("TABLES: %p %p\n", (void *)newTable, (void *)table);
    }
    return newTable;
}

void phylib_add_object( phylib_table *table, phylib_object *object ) {
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        //if nothing is null, nothing will happen
        if (table->object[i] == NULL) {
            table->object[i] = object;
            break; //cant fill in the other slots
        }
    }
}

void phylib_free_table( phylib_table *table ) {
    //frees the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) { //prevents issues with freeing a null object
            //printf("Freeing %p, %d: %d\n", (void *)table->object[i], i, table->object[i]->type);
            free(table->object[i]);
            table->object[i] = NULL;    
        }
    }

    free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
    phylib_coord difference;
    difference.x = (c1.x - c2.x);
    difference.y = (c1.y - c2.y);
    return difference;
}

double phylib_length(phylib_coord c) {
    //gets the length of phylib coord c (uses sqrt from math library)
    return sqrt((c.x * c.x) + (c.y * c.y));
}

double phylib_dot_product( phylib_coord a, phylib_coord b ) {
    //gets dot product of a, b
    return ((a.x * b.x)+ (a.y * b.y));
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) {
    //printf("Beginning distance\n");
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }

    if (obj2->type == PHYLIB_ROLLING_BALL || obj2->type == PHYLIB_STILL_BALL) {
        if (obj2->type == PHYLIB_ROLLING_BALL) {
            //printf("rolling ball reached\n");
            return phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos)) - PHYLIB_BALL_DIAMETER;
        } else {
            //printf("still ball reached\n");
            return phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER;
        }
        
    } else if (obj2->type == PHYLIB_HOLE) {
        //printf("hole reached\n");
        return phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;
    } else if (obj2->type == PHYLIB_HCUSHION || obj2->type == PHYLIB_VCUSHION) {
        phylib_coord v;
        if (obj2->type == PHYLIB_HCUSHION) {
            //printf("hcushion reached\n");
            v.x = 0;
            v.y = obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y;
        } else {
            //printf("vcushion reached\n");
            v.x = obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x;
            v.y = 0.0;
        }
        
        return phylib_length(v) - PHYLIB_BALL_RADIUS;
    } else {
        //printf("error: no class found reached\n");
        return -1.0;
    }
}

//HELPERS

//This is a helper function that returns a bool stating if the signs of two values are the same
int sameSign(double a, double b) {
    return ((a < 0.0) == (b < 0.0));
}

//BALL SIMULATION

void phylib_roll( phylib_object *new, phylib_object *old, double time ) {
    //printf("phylib_roll playing\n");
    if (new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL) {
        //printf("phylib_rolling\n");
        //printf("%p, %p", (void *)new, (void *)old);
        //big equation, simplify it first
        //note the new pointer might point to the same thing as old, so we record the old values first
        ;
        phylib_coord oldVel;
        oldVel.x = old->obj.rolling_ball.vel.x;
        oldVel.y = old->obj.rolling_ball.vel.y;
        phylib_coord oldPos;
        oldPos.x = old->obj.rolling_ball.pos.x;
        oldPos.y = old->obj.rolling_ball.pos.y;
        phylib_coord oldAcc;
        oldAcc.x = old->obj.rolling_ball.acc.x;
        oldAcc.y = old->obj.rolling_ball.acc.y;
        //update vel, pos
        new->obj.rolling_ball.vel.x = (oldVel.x) + (oldAcc.x * time);
        new->obj.rolling_ball.vel.y = (oldVel.y) + (oldAcc.y * time);
        
        new->obj.rolling_ball.pos.x = (oldPos.x) + (oldVel.x * time) + ((oldAcc.x * (time * time))/2);
        new->obj.rolling_ball.pos.y = (oldPos.y) + (oldVel.y * time) + ((oldAcc.y * (time * time))/2);
        //use helper function sameSign to see if we need to set to 0
        if (!sameSign(new->obj.rolling_ball.vel.x, oldVel.x)) {
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;
        }
        if (!sameSign(new->obj.rolling_ball.vel.y, oldVel.y)) {
            new->obj.rolling_ball.vel.y = 0.0;
            new->obj.rolling_ball.acc.y = 0.0;
        }
    }
}

unsigned char phylib_stopped( phylib_object *object ) {
    if (phylib_length(object->obj.rolling_ball.vel) >= PHYLIB_VEL_EPSILON) {
        /*For the purposes of this simulation a ball is considered to have stopped if its speed (which is the
length of its velocity) is less than PHYLIB_VEL_EPSILON.*/
        //printf("STOPPED: %f, %f", phylib_length(object->obj.rolling_ball.vel), phylib_length(object->obj.rolling_ball.acc));
        return 0;
    }
    //downgrade
    object->type = PHYLIB_STILL_BALL;

    object->obj.still_ball.number = object->obj.rolling_ball.number;
    object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
    object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;
    return 1;
}



void phylib_bounce( phylib_object **a, phylib_object **b ) {
    //complickated ahh function
    phylib_object * aReal = *a;
    phylib_object * bReal = *b;
    if (bReal->type == PHYLIB_HCUSHION) {
        //printf("COLLISION ON HCUSHION\n");
        //hcushion
        aReal->obj.rolling_ball.vel.y *= -1.0;
        aReal->obj.rolling_ball.acc.y *= -1.0;
    } else if (bReal->type == PHYLIB_VCUSHION) {
        //printf("COLLISION ON VCUSHION\n");
        //vcushion
        aReal->obj.rolling_ball.vel.x *= -1.0;
        aReal->obj.rolling_ball.acc.x *= -1.0;
    } else if (bReal->type == PHYLIB_HOLE) {
        //printf("COLLISION ON HOLE\n");
        //hole
        free(*a);
        *a = NULL;
        a = NULL;
    } else if (bReal->type == PHYLIB_STILL_BALL) {
        //printf("COLLISION ON STILL BALL\n");
        bReal->type = PHYLIB_ROLLING_BALL;
        //update our positional values accordingly
        bReal->obj.rolling_ball.number = bReal->obj.still_ball.number;
        bReal->obj.rolling_ball.pos.x = bReal->obj.still_ball.pos.x;
        bReal->obj.rolling_ball.pos.y = bReal->obj.still_ball.pos.y;

        //set our velocities and accelerations to 0 just to be sure
        bReal->obj.rolling_ball.acc.x = 0.0;
        bReal->obj.rolling_ball.acc.y = 0.0;

        bReal->obj.rolling_ball.vel.x = 0.0;
        bReal->obj.rolling_ball.vel.y = 0.0;
        //move to case 5
    }
    //no elses -> this can't be short circuited
    if (bReal->type == PHYLIB_ROLLING_BALL) {
        //printf("COLLISION ON ROLLING BALL %d to %d\n", aReal->obj.rolling_ball.number, bReal->obj.rolling_ball.number);
        //printf("BOUNCING BALL\n");
        phylib_coord r_ab = phylib_sub(aReal->obj.rolling_ball.pos, bReal->obj.rolling_ball.pos);
        phylib_coord v_rel = phylib_sub(aReal->obj.rolling_ball.vel, bReal->obj.rolling_ball.vel);
        phylib_coord n;
        //printf("r_ab = (%f, %f), v_rel = (%f, %f)\n", r_ab.x, r_ab.y, v_rel.x, v_rel.y);
        //n, r_ab
        n.x = r_ab.x / phylib_length(r_ab);
        n.y = r_ab.y / phylib_length(r_ab);
        double v_rel_n = phylib_dot_product(v_rel, n);
        //printf("n = (%f, %f), v_rel_n = %f\n", n.x, n.y, v_rel_n);
        aReal->obj.rolling_ball.vel.x -= v_rel_n * n.x;
        aReal->obj.rolling_ball.vel.y -= v_rel_n * n.y;

        bReal->obj.rolling_ball.vel.x += v_rel_n * n.x;
        bReal->obj.rolling_ball.vel.y += v_rel_n * n.y;
        //printf("a = (%f, %f), b = (%f, %f)\n",
        /*aReal->obj.rolling_ball.vel.x,
        aReal->obj.rolling_ball.vel.y,
        bReal->obj.rolling_ball.vel.x,
        bReal->obj.rolling_ball.vel.y
        );*/
        //use length to determine if we are above vel_epsilon and update accordingly
        double aLength = phylib_length(aReal->obj.rolling_ball.vel);
        double bLength = phylib_length(bReal->obj.rolling_ball.vel);
        if (aLength > PHYLIB_VEL_EPSILON) {
            aReal->obj.rolling_ball.acc.x = ((-1*(aReal->obj.rolling_ball.vel.x)) / aLength)*PHYLIB_DRAG;
            aReal->obj.rolling_ball.acc.y = ((-1*(aReal->obj.rolling_ball.vel.y)) / aLength)*PHYLIB_DRAG;
        }
        if (bLength > PHYLIB_VEL_EPSILON) {
            bReal->obj.rolling_ball.acc.x = ((-1*(bReal->obj.rolling_ball.vel.x)) / bLength)*PHYLIB_DRAG;
            bReal->obj.rolling_ball.acc.y = ((-1*(bReal->obj.rolling_ball.vel.y)) / bLength)*PHYLIB_DRAG;
        }
        //displace the positions of the balls so that they are farther apart (they can't collide again)

    }
}

unsigned char phylib_rolling( phylib_table *t ) {
    //rollin starts at 0
    unsigned char num = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        //for loop to each object, increment each object that is rolling for num
        if (t->object[i] != NULL) {
            if (t->object[i]->type == PHYLIB_ROLLING_BALL) {
                num++;
            }
        }
    }
    return num;
}

phylib_table *phylib_segment( phylib_table *table ) {
    //printf("Beginning phylib_segment\n");
    if (phylib_rolling(table) != 0) {
        //printf("phylib_rolling checked\n");
        phylib_table * copy_table = phylib_copy_table(table);
        //printf("TEST PRINT_TABLE FOR COPY_TABLE:\n");
        //phylib_print_table(copy_table); //TEST
        //printf("phylib_copy_table checked\n");
        //copy_table->time = 0;
        while (copy_table->time < PHYLIB_MAX_TIME) {
            copy_table->time += PHYLIB_SIM_RATE;
            //printf("TIME: %f ->", copy_table->time);
            //copy_table->time += PHYLIB_SIM_RATE;
            //apply phylib_roll to every ball
            for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
                if (copy_table->object[i] != NULL) {
                    if (copy_table->object[i]->type == PHYLIB_ROLLING_BALL) {
                        phylib_roll(copy_table->object[i], table->object[i], copy_table->time - table->time);
                    }
                }
            }
            for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
                if (copy_table->object[i] != NULL) {
                    //printf("Object not NULL\n");
                    if (copy_table->object[i]->type == PHYLIB_ROLLING_BALL) {
                        //check for phylib_bounce
                        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                            if (i != j) { 
                                if (copy_table->object[j] != NULL) {
                                    //printf("Trying phylib_distance on %d - %d\n", i, j);
                                    double dist = phylib_distance(copy_table->object[i], copy_table->object[j]);
                                    if (dist < 0.0 /*&& copy_table->time - table->time > PHYLIB_SIM_RATE*2*/) {
                                        //do a bounce     
                                        phylib_bounce(&(copy_table->object[i]), &(copy_table->object[j]));

                                        return copy_table;
                                    }
                                    
                                }  
                            }
                        }
                        //check for stop
                        if (phylib_stopped(copy_table->object[i])) {
                            return copy_table;
                        }
                    }
                }
            }
           
        }
        //printf("The table reached the max allotted time. TIME - %f\n", copy_table->time);
    }
    //printf("FINAL\n");
    //phylib_print_table(table);
    
    return NULL;
}

char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y );
                break;
                case PHYLIB_HCUSHION:
                snprintf( string, 80,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x );
            break;
    }
    return string;
}
