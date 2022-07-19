# Style Guide

This is largely based on [Airbnb's React/JSX Style Guide](https://github.com/airbnb/javascript/tree/master/react)

Here are a few things that are a little different or more explicit:

## Classes or functions

Please use functional components, and always define them using the `function` keyword.

eg:

```
// YES

function Listing({ hello }) {
    return <div>{hello}</div>;
}

// NO

const Listing = ({hello}) =>  {
    return <div>{hello}</div>;
}

```

This will help us make better use of ReactDevTools

## Naming files and directories

If a file contains a component then:

- It should only contain 1 component
- The file should have a `.jsx` extension
- If the file contains one dumb component (no use of hooks, redux or any other cleverness), just give the file the same name as the component itself. Eg `Button.jsx`

For more complex components (looks & cleverness), separate display from logic code into multiple files with the following naming conventions:

```
MyComponent/
index.jsx // the smarts go in here. This imports Presentation.jsx
    Presentaion.jsx // the good looks go here
    SomeDumbSubComponent.jsx // extra components used in the Presentation
    Presentation.stories.jsx // storybook things. We just make stories for Presentation, and other dumb components
    utils.js // sometimes a piece of js code doesn't fit neatly into a component file
```

## Code formatting

Code formatting and linting is not something a human should spend time on. Set up your editor so that it autoformats whenever you save a file.

If you are using vscode then install Prettier. Make sure your `settings.json` includes:

```
editor.defaultFormatter": "esbenp.prettier-vscode"
```

## Naming variables

```
import SomeComponent from "somewhere/SomeComponent"
import AnotherComponent from "somewhere/AnotherComponent"
...
const anotherComponentInstance = <AnotherComponent/>

<Foo
    userName="hello"
    phoneNumber={12345678}
    Component={SomeComponent} //notice the capital letter
    anotherComponentInstance={anotherComponentInstance} // and a small letter
/>
```

This makes sense if you think of Component functions as classes. They are used to instantiate things. If it walks like a class and quacks like a class, name it as though it’s a class.

## Arguments

By using objects and unpacking in our functions we make it possible to use propTypes effectively. Also swapping the order of arguments around shouldn’t matter.

```
// no
function foo(some,arguments,here){
    things
}

// yes - note the {}
function foo({some,arguments,here}){
    things
}
```

## Spreading objects with known explicit props

If the props are explicit, then it’s often preferable to handle them as a data structure (because that’s what they are) and then just pass the whole thing to the component using the spread operator.

```
// no
// always know what you are passing to a component

export default function Foo {
    ...
    return (<div {...mysteryProps} />);
}

// no
// this becomes hard to read if there are lots of props

export default function Foo {
    return (<div
        text={''}
        isPublished={false}
        some={some}
        other={other}
        stuff={stuff}
        blah={blah}
        etc={etc}
    />);
}

// Yes

export default function Foo {
    const props = {
        text: '',
        isPublished: false,
        some,
        other,
        stuff,
        blah,
        etc
    }

    return (<div {...props} />);
}
```

## Importing things

**Use path imports**(whenever possible) for importing components, icons, etc. from external libraries. This is so the bundle size remains small because we won't be loading the whole library.

```
// No

import { Button, TextField } from "@mui/material";

// Yes

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
```

Note: In some cases it won't matter since most bundlers support [tree shaking](https://en.wikipedia.org/wiki/Tree_shaking) out of the box.
