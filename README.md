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
- **v0.1.3**, *22 November 2012*
  - Fixed issue #2 and #3, autoDocBlockr now triggers only on function declarations and function statements in JS.

- **v0.1.2**, *19 November 2012*
  - Fixed issue #1, regex problem for fetching params in parser module.

## License

[MIT License](http://en.wikipedia.org/wiki/MIT_License)
© [Thanasis Polychronakis](https://github.com/thanpolas)
