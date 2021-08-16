# Creating NodeJS addon and building it with node-gyp in Windows example

1. Clone this repo.
2. Run `npm install`. You'll see that the automatic build of the addon fails due to unresolvable path. This is a bug after node-gyp v4.0.0.
3. Install `npm i -g node-gyp@4.0.0` and then `node-gyp rebuild`. The error does not persist.
4. Run `node index.js` to execute the addon using javascript.


### High level overview of the node-gyp's Workflow

A `binding.gyp` file describes the configuration to build your module, in a JSON-like format. 
This file gets placed in the root of your package, alongside `package.json`.

`node-gyp rebuild` does the following all in a row:
- calls `clean`
- calls `configure`
- calls `build`

`configure` generates the appropriate project build files for the current platform.  The configure step looks for a 
`binding.gyp` file in the current directory to process.

If `configure` step completed you will have either a Makefile (on Unix platforms) or a vcxproj file (on Windows) in the build/ directory.

After running `node-gyp build` you have your compiled .node bindings file! 
The compiled bindings end up in build/Debug/ or build/Release/, depending on the build mode. 
At this point, you can require the .node file with Node.js  


## File path **BUG** version > 4.0.0

As can be seen from [binding.gyp](./binding.gyp) file there is a special `action` defined. 
Actions can be anything. For this example it's just executing a [Python code](./deps/hello-world.py) to print "Hello World!".  

When running `install` script `node-gyp` runs `configure` command to generate project files (`sln`, `vcxproj`) for building with MS build tools.

The generated file has one action path misconfigured:

```
<Command>call call python &quot;deps/hello-world.py&quot;&#xD;&#xA;if %errorlevel% neq 0 exit /b %errorlevel%</Command>
```

With `node-gyp@4.0.0` this is not the case:

```
<Command>call call python &quot;..\deps\hello-world.py&quot;&#xD;&#xA;if %errorlevel% neq 0 exit /b %errorlevel%</Command>
```

Clearly something is off with the file paths handling. I suspect `gyp` written in Python to be the culprit.

### Workaround

Found that providing absolute path in `binding.gyp` file solves the issue. At least with the latest `node-gyp@8.1.0`

```
'inputs': [
  '<(module_root_dir)/deps/hello-world.py'
]
```

Note the added `<(module_root_dir)`.



