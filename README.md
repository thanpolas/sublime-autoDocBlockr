# Automatic Document Block Insertion

autoDocBlockr will insert document blocks automatically. Just move over your functions and autoDocBlockr will read if the function has any document blocks, check if they are ok and if not properly modify them.

It is triggered seemlesly as you move your cursor through a function declaration.

## Instalation

Go to your sublime packages folder and:

```shell
clone git@github.com:thanpolas/sublime-autoDocBlockr.git autoDocBlockr
```

## Dependencies

This package depends on [docBlockr](https://github.com/spadgos/sublime-jsdocs), a stripped version is included inside the `autoDocBlockr` package.

## Changelog
- **v0.1.5**, *23 November 2012*
  - Fixed issue #7 and #9, when no docBlock exists and a new one is created, the cursor was not positioned properly.
  - Fixed issue #8, updated the @param docBlock parser regex to match edge cases.

- **v0.1.4**, *22 November 2012*
  - Fixed issue #2 and #3, autoDocBlockr now triggers only on function declarations and function statements in JS.
  - Fixed issue #4, not properly handling multiline @param statements.

- **v0.1.2**, *19 November 2012*
  - Fixed issue #1, regex problem for fetching params in parser module.

## License

[MIT License](http://en.wikipedia.org/wiki/MIT_License)
© [Thanasis Polychronakis](https://github.com/thanpolas)
