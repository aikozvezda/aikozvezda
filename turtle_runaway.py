# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer1 = turtle.RawTurtle(canvas)
        self.drawer1.hideturtle()
        self.drawer1.penup() 
        
        self.drawer2 = turtle.RawTurtle(canvas)
        self.drawer2.hideturtle()
        self.drawer2.penup() 
        
        self.drawer3 = turtle.RawTurtle(canvas)
        self.drawer3.hideturtle()
        self.drawer3.penup() 
        
        self.drawer2 = turtle.RawTurtle(canvas)    
        self.drawer2.hideturtle()
        self.drawer2.speed(0)
        self.drawer2.penup()
        self.drawer2.setpos(300,-300)
        self.drawer2.pendown()
        self.drawer2.setheading(90)
        for i in range(4):
            self.drawer2.forward(600)
            self.drawer2.left(90)
            
            
    def is_catched(self):
        p = self.chaser.pos()
        q = self.runner.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
        

    def start(self, init_dist=400, ai_timer_msec=100, score=0):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.score=score #
        self.start_time=time.time() #
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        
        if (self.chaser.xcor()<-300 or self.chaser.xcor()>300):
            self.score=self.score-3
        if (self.chaser.ycor()<-300 or self.chaser.ycor()>300):
            self.score=self.score-3
            
            # TODO) You can do something here and follows.            
        if self.is_catched()==True:
            self.score += 1
        
        elapse=time.time()-self.start_time
         
        # Note) The following line should be the last of this function to keep the game playing
        #draw elapsed time
        self.drawer1.undo()
        self.drawer1.penup()
        self.drawer1.setpos(-430, 150)
        self.drawer1.write(f'Time {elapse:.0f}', font={'Arial',12})  
       
        #draw score
        self.drawer2.undo()
        self.drawer2.penup()
        self.drawer2.setpos(-430,100)
        self.drawer2.write(f'Score {self.score}',font={'Arial',12})
       
        #draw game_status
        self.drawer3.undo()
        self.drawer3.penup()
        self.drawer3.setpos(-430,50)
        self.drawer3.write('In game',font={'Arial',12})
         
               
        if elapse>100:
            self.drawer3.undo()
            self.drawer3.write("Game Over",font={'Arial',12})
            return
        
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    root.title('Turtle Runaway')        
    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    canvas.mainloop()
