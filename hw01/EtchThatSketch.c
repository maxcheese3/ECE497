/*
 * Etch That Sketch
 * Simple screen drawing program created by Ryan Evans.
 * Controls are WASD for movement. C for clear. X for exit.
 * Has configureable WIDTH and HEIGHT settings.
 * Compile with gcc -o <desiredname> EtchThatSketch.c -l ncurses
 * September 3, 2017
 */

#include <ncurses.h>
int main()
{
	int WIDTH = 16;			//Number of columns
	int HEIGHT = 16;			//Number of rows
	int x = 0;			//Cursor x coordinate
	int y = HEIGHT;			//Cursor y coordinate
	
	initscr(); 			//initialize
	cbreak();			//can exit with ^C, Don't require Enter to be hit
	noecho();			//Don't echo keypresses
	curs_set(0);			//Hide the curso (providing terminal supports it)
	mvaddch(y,x,'*');		//Move cursor to bottom

	while (1){
	char c = getch();
	if (c == 'a'){
		//Check if can decrement x, if can, do it
		if (x > 0){
			x-=1;
			mvaddch(y,x,'*');
			refresh();
		}	
	}
	else if (c == 'd'){
		//Check if can increment x, if can, do it
		if (x < WIDTH){
			x+=1;
			mvaddch(y,x,'*');
			refresh();
		}	
	}
	else if (c == 'w'){
		//Check if can decrement y, if can, do it
		if (y > 0){
			y-=1;
			mvaddch(y,x,'*');
			refresh();
		}	
	}
	else if (c == 's'){
		//Check if can increment y, if can, do it
		if (y < HEIGHT){
			y+=1;
			mvaddch(y,x,'*');
			refresh();
		}	
	}
	else if (c == 'c'){
		//Clear the screen
		clear();
	}
	else if (c == 'x'){
		//exit
		break;
	}
	}

	endwin();			//closes down library
	return 0;
}
