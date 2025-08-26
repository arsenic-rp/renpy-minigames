init python:

    def apply_mask(mask):
        return lambda child: AlphaMask(child, mask)
        
    def trace(anchor=(0,0), init_xy=(0,0)):
        return lambda child: Tracer(child, anchor, init_xy)
        
    def zoomtrace(zoom=1.0, shift=(0,0), borders=True, init_xy=(0,0)):
        return lambda child: ZoomTracer(child, zoom, shift, borders, init_xy)

    class Tracer(renpy.Displayable):
        def __init__(self, child, anchor=(0,0), init_xy=(0,0)):
            super(Tracer, self).__init__()
            self.child = renpy.displayable(child)
            self.x, self.y = init_xy
            self.anchor = anchor
            
        def visit(self):
            return [self.child]
            
        def event(self, ev, x, y, st):
            import pygame
            if (ev.type == pygame.MOUSEMOTION) or (ev.type == pygame.MOUSEBUTTONDOWN):
                if x is not None: self.x = x
                if y is not None: self.y = y
                
        def render(self, width, height, st, at):
 
            cr = renpy.render(self.child, width, height, st, at)
            cw, ch = cr.get_size()

            dx, dy = 0,0
            ax, ay = self.anchor
            
            if isinstance(ax, int):
                dx = ax
            else:
                dx = ax * cw
                
            if isinstance(ay, int):
                dy = ay
            else:
                dy = ay * ch
 
            rv = renpy.Render(cw, ch)
            
            rv.blit(cr, (self.x-dx, self.y-dy))
            renpy.redraw(self, 0.0)
            return rv
            

    class ZoomTracer(renpy.Displayable):
            def __init__(self, child, zoom=1.0, shift=(0,0), borders=True, init_xy = (0,0)):
                super(ZoomTracer, self).__init__()
                self.child = At(renpy.displayable(child), Transform(zoom=zoom))
                self.x, self.y = init_xy
                self.zoom = zoom
                self.shiftx, self.shifty = shift
                self.borders = borders
                
            def visit(self):
                return [self.child]
                
            def event(self, ev, x, y, st):
                import pygame
                if (ev.type == pygame.MOUSEMOTION) or (ev.type == pygame.MOUSEBUTTONDOWN):
                    if x is not None: self.x = x
                    if y is not None: self.y = y
                    
            def render(self, width, height, st, at):
     
                cr = renpy.render(self.child, width, height, st, at)
                cw, ch = cr.get_size()
     
                rv = renpy.Render(width, height) #renpy.Render(cw, ch)
                
                xx = self.x + self.shiftx
                yy = self.y + self.shifty
                
                if self.borders:
                    xx = min(max(xx,0),1920)
                    yy = min(max(yy,0),1080)
                
                dx = xx * (1.0 - self.zoom)
                dy = yy * (1.0 - self.zoom)
                
                rv.blit(cr, (dx,dy))
                renpy.redraw(self, 0.0)
                return rv
