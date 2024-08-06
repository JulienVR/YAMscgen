# YAMscgen

### Generating an example file

Copy paste this in a `input.txt` file. Note that this example also works with Mscgen.

```
msc {
    # Global options here
    arcgradient="10";
    
    # Entities here
    a [label="Entity A", textbgcolor="#82b366"],
    b [label="Entity B", textbgcolor="grey"],
    c [label="Entity C", textbgcolor="#d79b00"];
    
    # Arcs, boxes
    
    # A line finishes with ';'
    a => b [label="First call"];
    
    # Several elements can be aligned
    b => b [label="Processing...", textbgcolor="yellow"], 
    c note c [label="Several elements\ncan be on the\nsame line", textbgcolor="#dae8fc"];
    
    c -> b [label="Another arc type"];
    b >> a [label="A dashed arc\nis useful here"],
    c rbox c [label="This is another\ntype of comment", textbgcolor="#dae8fc"];
    
    ... [label="Time flies...", textcolor="blue"];
    
    a -x b [label="And this is an\nlost arc"];
    a -> c [label="Last call", linecolor="red"];
}
```

Now, execute

```
$ python3 yamscgen.py -i input.txt -o out.svg
```

![Demo diagram](https://github.com/JulienVR/YAMscgen/blob/main/demo.png "Demo diagram")

### Fonts

You can use any font from `Courier`, `Helvetica`, `Times`.

Set the font globally, e.g. `font="Helvetica";`.
You can also set the font on a given element, e.g. `a->b [label="test", font-family="Courier"]`.

The reason `font-family` is used on the element level is that it is the name of the SVG attribute for a `text` node.
You can also pass any SVG attribute to the elements, they will be passed to the SVG. 
For instance: `font-weight="bold"` or `font-style="italic"`.


### Splitting on multiple files

Add `max-height="250"` to the global options in the `input.txt` to obtain:

```
msc {
    # Global options here
    arcgradient="10", max-height="250";
    
    # Entities here
    a [label="Entity A", textbgcolor="#82b366"],
    b [label="Entity B", textbgcolor="grey"],
    c [label="Entity C", textbgcolor="#d79b00"];
    
    # Arcs, boxes
    
    # A line finishes with ';'
    a=>b [label="First call"];
    
    # Several elements can be aligned
    b=>b [label="Processing...", textbgcolor="yellow"], 
    c note c [label="Several elements\ncan be on the\nsame line", textbgcolor="#dae8fc"];
    
    c -> b [label="Another arc type"];
    b >> a [label="A dashed arc\nis useful here"],
    c rbox c [label="This is another\ntype of comment", textbgcolor="#dae8fc"];
    
    ... [label="Time flies...", textcolor="blue"];
    
    a:>b [label="And this is an\nemphasized arc"];
    a->c [label="Last call", linecolor="red"];
}
```

After running again `$ python3 yamscgen.py -i input.txt -o out.svg`, 2 diagrams should have been created.


### Adding a CSS file

Copy paste this in a `template.css` file.

```css
/* color the lifeline of A in green */
.lifelines > line.a, g.participants  > rect.a{
    stroke: green;
}

/* color the lifeline of B in blue */
.lifelines > line.b, g.participants  > rect.b {
    stroke: blue;
}

/* color the arcs */
.elements > line, .elements > path,  .elements > rect {
    stroke: orange;
}

/* color the tip of the arrows */
defs path {
    stroke: orange;
    fill: orange;
}

/* highlight all labels of the 4th line */
#line-4 .label > rect {
    fill: greenyellow;
}
```

Now, execute

```
$ python3 yamscgen.py -i input.txt -c template.css -o out.svg
```

![Demo diagram with CSS](https://github.com/JulienVR/YAMscgen/blob/main/demo_css.png "Demo diagram with CSS")