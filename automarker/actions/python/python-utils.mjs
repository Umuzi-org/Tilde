/*
Sometimes there is stderr output without there being actual errors 

    // # eg
    //   '[notice] A new release of pip is available: 23.2.1 -> 23.3\n' +
    // '[notice] To update, run: pip install --upgrade pip\n' +
    // '\n' +
    // '[notice] A new release of pip is available: 23.2.1 -> 23.3\n' +
    // '[notice] To update, run: pip install --upgrade pip"}'
*/
export function stdoutHasErrors({ scriptErrorOutput }) {
  // const scriptErrorOutput = await shell.exec(command).stderr.trim();

  const scriptErrorOutputLines = scriptErrorOutput
    .split("\n")
    .filter((l) => l.length)
    .filter((l) => !l.startsWith("[notice]"));

  if (scriptErrorOutputLines.length) {
    return true;
  }
  return false;
}
