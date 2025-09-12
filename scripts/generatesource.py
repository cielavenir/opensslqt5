#!/usr/bin/python

import os.path
import subprocess

with open(os.path.join(os.path.dirname(__file__), 'symbols_ssl.txt'), 'r') as f:
    symbols_ssl = list(map(str.rstrip, f.readlines()))

with open(os.path.join(os.path.dirname(__file__), 'symbols_crypto.txt'), 'r') as f:
    symbols_crypto = list(map(str.rstrip, f.readlines()))

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), '../src/libopensslqt5.c'), 'w') as f:
        f.writelines([
            '#include <dlfcn.h>\n',
            '\n',
            '#pragma GCC visibility push(hidden)\n',
            'void *ptr_libssl;\n',
            'void *ptr_libcrypto;\n',
        ] + [
            'void *ptr_' + symbol + ';\n' for symbol in symbols_ssl + symbols_crypto
        ] + [
            '#pragma GCC visibility pop\n',
            '\n',
            '__attribute__((constructor,visibility("hidden"))) void init(){\n',
            '    ptr_libssl = dlopen("libssl.so.1.1", RTLD_NOW);\n',
            '    ptr_libcrypto = dlopen("libcrypto.so.1.1", RTLD_NOW);\n',
        ] + [
            '    ptr_%s = dlsym(ptr_libssl, "%s");\n' % (symbol, symbol) for symbol in symbols_ssl
        ] + [
            '    ptr_%s = dlsym(ptr_libcrypto, "%s");\n' % (symbol, symbol) for symbol in symbols_crypto
        ] + [
            '}\n',
            '\n',
            '__attribute__((destructor,visibility("hidden"))) void fini(){\n',
            '    if(ptr_libcrypto)dlclose(ptr_libcrypto);\n',
            '}\n',
            '\nint impl_ossl_statem_in_error(){return 0;}\n__asm__(".symver impl_ossl_statem_in_error,ossl_statem_in_error@@Qt_5");\n',
        ] + [
            '\nvoid impl_%s(){__asm__("jmp ptr_%s;");}\n__asm__(".symver impl_%s,%s@@Qt_5");\n' % (symbol, symbol, symbol, symbol) for symbol in symbols_ssl + symbols_crypto
        ])

    with open(os.path.join(os.path.dirname(__file__), '../src/libopensslqt5.map'), 'w') as f:
        f.writelines([
            'Qt_5 {\n',
            'global:\n',
            'ossl_statem_in_error;\n',
        ] + [
            symbol + ';\n' for symbol in symbols_ssl + symbols_crypto
        ] + [
            'local:\n',
            '*;\n',
            '};\n',
        ])

    subprocess.check_call(['gcc', '-O', '-fPIC', '-shared', '-Wl,--no-undefined', '-Wl,--version-script,' + os.path.join(os.path.dirname(__file__), '../src/libopensslqt5.map'), os.path.join(os.path.dirname(__file__), '../src/libopensslqt5.c'), '-o', 'libopensslqt5.so', '-ldl'])
