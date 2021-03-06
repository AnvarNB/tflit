'''


Version Info: https://www.tensorflow.org/lite/guide/python

To get URLs: `$('.devsite-table-wrapper').find('a').map((i, e) => e.href).get()`

And to add jQuery
```javascript
var jq = document.createElement('script');
jq.onload = function() { jQuery.noConflict(); $ = jQuery; }
jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(jq);
```

[
    # Linux ARM 32
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp35-cp35m-linux_armv7l.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-linux_armv7l.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp38-cp38-linux_armv7l.whl",
    # Linux ARM 64
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp35-cp35m-linux_aarch64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-linux_aarch64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_aarch64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp38-cp38-linux_aarch64.whl",
    # Linux x86-64
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp35-cp35m-linux_x86_64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-linux_x86_64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_x86_64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp38-cp38-linux_x86_64.whl",
    # Mac 10.14
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp35-cp35m-macosx_10_14_x86_64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-macosx_10_14_x86_64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-macosx_10_14_x86_64.whl",
    # Windows 10
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp35-cp35m-win_amd64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-win_amd64.whl",
    "https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-win_amd64.whl"
]

'''

URL = (
    'https://dl.google.com/coral/python/tflite_runtime-'
    '{version}-cp{py}-cp{pym}-{platform}_{arch}.whl')

PLATFORMS = {
    'Linux': 'linux',
    'Darwin': 'macosx',
    'Windows': 'win',
}

VERSIONS = {
    'Linux': ['35', '36', '37', '38'],
    'Darwin': ['35', '36', '37'],
    'Windows': ['35', '36', '37'],
}
NO_M = ['38']

MAC_VERSION = 10, 14

def get_tflite_url(version='2.1.0.post1'):
    import sys
    import platform

    system = platform.system()
    platfm = PLATFORMS.get(system)
    arch = platform.uname()[4]  # .machine
    py_version = '{}{}'.format(*sys.version_info)

    if system == 'Linux':
        pass
    elif system == 'Darwin':
        platfm += '_' + '_'.join(map(str, MAC_VERSION))
    elif system == 'Windows':
        pass
    else:
        raise ValueError('Unknown system: {}'.format(system))

    return URL.format(
        version=version, py=py_version,
        pym=py_version if py_version in NO_M else py_version + 'm',
        platform=platfm,
        arch=arch,
    )



# Fuck it. Pypi you gave me no other choice. You said:
#   ERROR: Packages installed from PyPI cannot depend on packages which are not also hosted on PyPI.
# so I say asdfkadsljsldkfjklsdjflka eat shit. Imma do it anyways. (╯°□°）╯︵ ┻━┻
# apparently this is the recommended way anyways: https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program
def install(verbose=False, **kw):
    import sys
    import subprocess
    url = get_tflite_url(**kw)
    if verbose:
        print('Getting tflite from:', url)
    output = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', url],
        check=False,
        stdout=sys.stdout if verbose else subprocess.PIPE,
        stderr=sys.stderr)
    if verbose:
        print(output)
    output.check_returncode()

def check_install(verbose=False, **kw):
    USER_MESSAGE = (
        "NOTE: The reason that this is even necessary is because tensorflow still "
        "hasn't released tflite_runtime on pypi and pypi freaks out if "
        "a url outside of pypi is included as a dependency. "
        "Once this upstream issue is resolved this message will go away.")
    try:
        import tflite_runtime
    except ImportError as e:
        print(e, 'installing the right version for your system now...')
        if verbose:
            print(USER_MESSAGE)
        install(verbose=verbose, **kw)
        if verbose:
            print('.'*50)
        print('All done! Carry on.')


if __name__ == '__main__':
    import fire
    fire.Fire(check_install)
