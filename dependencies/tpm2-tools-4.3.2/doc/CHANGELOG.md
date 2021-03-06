## Changelog

### 4.3.2 2021-06-21

  * tpm2_import: fix fixed AES key CVE-2021-3565
      - tpm2_import used a fixed AES key for the inner wrapper, which means that
        a MITM attack would be able to unwrap the imported key. To fix this,
        ensure the key size is 16 bytes or bigger and use OpenSSL to generate a
        secure random AES key.

### 4.3.1 2021-05-18

  * tpm2_dictionarylockout: Fix issue where setting value reset others

  * tpm2_create.c: Fix an issue where userwithauth attr cleared if policy
    specified

  * tss2_quote: Tool now correctly supports to quote against a list of passed
    PCR registers

  * Fix fapi-branch-select integration test to correctly use the PolicyRef
    parameter (triggered by recent bug-fix in tpm2-tss)

  * Fix an outdated parameter in the fapi-provision integration test

  * tpm2_getekcertificate: Fix tool failing to return error/non-zero
    for HTTP 404

### 4.3.0 - 2020-08-24

 * tss2_*: Fix double-free errors in commands asking for password authorization

 * tss2_*: Fix shorthand command -f that was falsely requiring an argument

 * tss2_*: Update tss2_encrypt to the new FAPI interface
   - The argument 'policyPath' is removed which was never read anyway

 * tss2_*: Remove the additional '\n' that was appended when redirecting to stdout

 * tss2_*: Update mandatory vs optional treatment of arguments according to latest Fapi spec

 * tss2_*: tss2_getinfo now retrieves the correct FAPI version from Fapi_GetInfo

 * tss2_*: Fix the error handling in case of multiple inputs and/or outputs from stdin/stdout

 * tss2_*: Fix syntax errors and update content of man pages according to latest Fapi spec

 * tss2_*: Add parameter types to all man page

 * tss2_*: tss2_setappdata now reads from file or stdin allowing to store also binary data

 * tss2_*: Memory leaks are fixed in cases when a returned empty non-char output value was passed to file output

 * tss2_pcrextend: fix extending PCR 0

 * tss2_quote: fix unused TSS2_RC in LOG_ERR

### 4.2.1 - 2020-05-25

* Fix missing handle maps for ESY3 handle breaks. See #1994.

* Bump ESYS minimum dependency version from 2.3.0 to 2.4.0.

* Fix for loop declarations build error.

### 4.2 2020-04-08

 * Fix various issues reported by static analysis tools.

 * Add integration test for ECC based getekcertificate.

 * Fix for issue #1959 where ARM builds were failing.

 * Add a check in autotools to add "expect" as a package dependency for fapi tools.

 * tpm2_createek: Drop the unused -p or --ek-auth option

 * tpm2_policyor: List of policy files should be specified as an argument
   instead of -l option. The -l option is still retained for backwards
   compatibility. See issue#1894.

 * tpm2\_eventlog: add a tool for parsing and displaying the event log.

 * tpm2_createek: Fix an issue where the `template` option looked for args

 * tpm2_hierarchycontrol: Fixed bug where tool operation failed silently

 * tpm2_nvdefine: Fixed an issue where text output suggested failures as passes

 * tpm2_certify: Add an example usage in man page

 * tpm2_policyor: Fix a bug where tool failed silently when no input were given

 * tpm2_getekcertificate: Intel (R) PTT EK cert web portal is set as default address

 * tpm2_alg_util.c: Fix a bug where string rsa3072 was not parsed

 * .ci/download-deps.sh: Change tss dependency to 2.4.0 to acquire SAPI handles for cpHash calculations

 * tpm2_policycphash: Add a tool to implement enhanced authorization with cpHash of a command

 * Add options to tools to enable cpHash outputs: tpm2_nvsetbits, tpm2_nvextend,
   tpm2_nvincrement, tpm2_nvread, tpm2_nvreadlock, tpm2_writelock, tpm2_nvdefine,
   tpm2_nvundefine, tpm2_nvcertify, tpm2_policynv, tpm2_policyauthorizenv,
   tpm2_policysecret, tpm2_create, tpm2_load, tpm2_activatecredential, tpm2_unseal,
   tpm2_changeauth, tpm2_duplicate, tpm2_import, tpm2_rsadecrypt, tpm2_certify,
   tpm2_certifycreation, tpm2_hierarchycontrol, tpm2_setprimarypolicy, tpm2_clearcontrol,
   tpm2_dictionarylockout, tpm2_evictcontrol, tpm2_setclock, tpm2_clockrateadjust,
   tpm2_clear, tpm2_nvwrite, tpm2_encryptdecrypt, tpm2_hmac.

 * tpm2_import: Fix an issue where the imported key always required to have a policy

 * tpm2_policysecret: Fix an issue where authorization model was fixed to password only

 * Feature API (FAPI) tools added. These additional set of tools implement utilities
   using the FAPI which was added to the tpm2-tss v2.4.4:
   tss2_decrypt, tss2_encrypt, tss2_list, tss2_changeauth, tss2_delete,
   tss2_import, tss2_getinfo, tss2_createkey, tss2_createseal, tss2_exportkey,
   tss2_getcertificate, tss2_getplatformcertificates, tss2_gettpmblobs,
   tss2_getappdata, tss2_setappdata, tss2_setcertificate, tss2_sign,
   tss2_verifysignature, tss2_verifyquote, tss2_createnv, tss2_nvextend,
   tss2_nvincrement, tss2_nvread, tss2_nvsetbits, tss2_nvwrite,
   tss2_getdescription, tss2_setdescription, tss2_pcrextend, tss2_quote,
   tss2_pcrread, tss2_authorizepolicy, tss2_exportpolicy, tss2_import,
   tss2_provision, tss2_getrandom, tss2_unseal, tss2_writeauthorizenv

 * tpm2_policycountertimer: Fix an issue where operandB array was reversed causing faulty comparisons.

### 4.1.1 - 2020-01-21

* tpm2\_certify: Fix output of attestation data including size field. Now outputs just bytes.
* tpm2\_certifycreation: Fix tool to match manpage where the code had the -C and -c options reversed.
* tpm2\_gettime: Fix output of attestation data including size field. Now outputs just bytes.
* tpm2\_nvcertify: Fix output of attestation data including size field. Now outputs just bytes.
* tpm2\_nvreadpublic: add name hash output.
* tpm2\_import: Support object policies when importing raw key material.
* Fix overflow in pcrs.h where sizeof() was used instead of ARRAY\_LEN().
* build:
  - Fix compilation issue: lib/tpm2\_hash.c:17:19: note: 'left' was declared here.
* man:
    - Fix manpage examples that have "sha" instead of "sha1"
    - tpm2\_shutdown manpage was missing, add it to build.
    - Fix manpage example for tpm2\_createak's tpm2\_evictcontrol example.

### 4.1 2019-11-25

* tpm2\_certifycreation: New tool enabling command TPM2\_CertifyCreation.

* tpm2\_checkquote:
   - Fix YAML output bug.
   - \-g option for specifying hash algorithm is optional and defaults to
     sha256.

* tpm2\_changeeps: A new tool for changing the Endorsement hierarchy primary seed.

* tpm2\_changepps: A new tool for changing the Platform hierarchy primary seed.

* tpm2\_clockrateadjust: Add a new tool for modifying the period on the TPM.

* tpm2\_create: Add tool options for specifying output data for use in
certification
  - \--creation-data to save the creation data
  - \--creation-ticket or -t to save the creation ticket
  - \--creation-hash or -d to save the creation hash
  - \--template-data for saving the template data of the key
  - \--outside-info or -q for specifying unique data to include in creation data.
  - \--pcr-list or -l  Add option to specify pcr list to add to creation data.

* tpm2\_createprimary: Add tool options for specifying output data for use
  in certification
  - \--creation-data to save the creation data
  - \--creation-ticket or -t to save the creation ticket
  - \--creation-hash or -d to save the creation hash
  - \--template-data for saving the template data of the key
  - \--outside-info or -q for specifying unique data to include in creation data.
  - \--pcr-list or -l  Add option to specify pcr list to add to creation data.

* tpm2\_evictcontrol:
    - Fix bug in automatic persistent handle selection when
      hierarchy is platform.
    - Fix bug in YAML key action where action was wrong when using ESYS\_TR.

* tpm2\_getcap: clean up remanenats of -c option in manpages and tool output.

* tpm2\_gettime: Add a new tool for retrieving a signed timestamp from a TPM.

* tpm2\_nvcertify: Add a new tool for certifying the contents of an NV index.

* tpm2\_nvdefine:
  - Support default set of attributes so -a is not mandatory.
  - Support searching for free index if an index isn't specified.

* tpm2\_nvextend: Add a new tool for extending an NV index similair to a PCR.

* tpm2\_nvreadpublic:
  - Support specifying nv index to read public data from as argument.

* tpm2\_nvsetbits: Add a new tool for setting the values of PCR with type
    "bits".

* tpm2\_nvundefine: Add support for deleting NV indices with attribute
    `TPMA_NV_POLICY_DELETE` set using NV Undefine Special command.

* tpm2\_nvwritelock: Add a new tool for setting a write lock on an NV index
    or globally locking nv indices with TPMA\_NV\_GLOBALLOCK.

* tpm2\_policyauthorizenv: New tool enabling signed, revocable policies.

* tpm2\_policyauthvalue: New tool enabling authorization to be bound to the
    authorization of another object.

* tpm2\_policycountertimer: Add a new tool for enabling policy bound to TPM
  clock or timer values.

* tpm2\_policynamehash: Add a new tool for specifying policy based on object
  name.

* tpm2\_policynv: Add a new tool for specifying policy based on NV contents.

* tpm2\_nvwritten: Add a new tool for specifying policy based on whether or not
    an NV index was written to.

* tpm2\_policysecret: Add tool options for specifying
  - \--expiration or -t
  - \--ticket
  - \--timeout
  - \--nonce-tpm or -x
  - \--qualification or -q

* tpm2\_policysigned: New tool enabling policy command TPM2\_PolicySigned.

* tpm2\_policytemplate: New tool enabling policy command TPM2\_PolicyTemplate.

* tpm2\_policyticket: New tool enabling policy command TPM2\_PolicyTicket.

* tpm2\_readclock: Add a new tool for reading the TPM clock.

* tpm2\_setclock: Add a new tool for setting the TPM clock.

* tpm2\_setprimarypolicy: New tool setting policy on hierarchies.

* tpm2\_shutdown: Add a new tool for issuing a TPM shutdown command.

* misc:
  - Support "tpmt" as a public key output format that only saves the TPMT
  structure.
  - Qualifying data or extra data in many tools can be hex array string or
  binary file.
  - Add support for specifying NV index type when specifying NV attributes.
  - Support added for tools to run on FreeBSD.
  - Skip and notify of action that man pages will not install if the package
  pandoc is missing.
  - Fix precedence issue with bitwise operator order int tpm2_getcap
  - travis: bump abrmd version 2.3.0
  - tpm2_util.c: Fix an issue int variable size was checked against uint
  - pcr.c: Fix buffer length issue to support all defined hash algorithm

### 4.0.1 - 2019-10-28

tpm2_checkquote:
  Fix YAML output bug.

### 3.2.1 - 2019-10-10

* Fix invalid memcpy when extracting ECDSA plain signatures.
* Fix resource leak on FILE * in hashing routine.
* Correct PCR logic to prevent memory corruption bug.
* Errata handler fix.

### 4.0 - 2019-09-09

* tpm2_activatecredential:
  - \--context is now \--credentialedkey-context.
  - \--key-context is now \--credentialkey-context.
  - \--Password is now \--credentialedkey-auth.
  - \--endorse-passwd is now \--credentialkey-auth.
  - \--in-file is now \--credential-secret.
  - \--out-file is now \--certinfo-data.
  - -f becomes -i.
  - -k becomes -C.
  - -e becomes -E.

* tpm2_certify:
  - \--halg is now \--hash-algorithm.
  - \--obj-context is now \--certifiedkey-context.
  - \--key-context is now \--signingkey-context.
  - \--pwdo is now \--certifiedkey-auth.
  - \--pwdk is now \--signingkey-auth.
  - -a becomes -o.
  - -k becomes -p.
  - -c becomes -C.
  - -k becomes -K.

* tpm2_changeauth:
  - New tool for changing the authorization values of:
    - Hierarchies
    - NV
    - Objects
  - Replaces tpm2_takeownership with more generic functionality.

* tpm2_checkquote:
  - \--halg is now \--hash-algorithm.
  - \--pcr-input-file is now \--pcr.
  - \--pubfile is now \--public.
  - \--qualify-data is now \--qualification.
  - -f becomes -F.
  - -F becomes -f.
  - -G becomes -g.

* tpm2_clear:
  - \--lockout-passwd is now \--auth-lockout.

* tpm2_clearcontrol:
  - New tool for enabling or disabling tpm2_clear commands.

* tpm2_create
  - \--object-attributes is now \--attributes.
  - \--pwdp is now \--parent-auth.
  - \--pwdo is now \--key-auth.
  - \--in-file is now \--sealing-input.
  - \--policy-file is now \--policy.
  - \--pubfile is now \--public.
  - \--privfile is now \--private.
  - \--out-context is now \--key-context.
  - \--halg is now \--hash-algorithm.
  - \--kalg is now \--key-algorithm.
  - -o becomes -c.
  - -K becomes -p.
  - -A becomes -b.
  - -I becomes -i.
  - -g becomes an optional option.
  - -G becomes an optional option.
  - Supports TPM command CreateLoaded via -c.

* tpm2_createak:
  - Renamed from tpm2_getpubak

* tpm2_createek:
  - renamed from tpm2_getpubek

* tpm2_createpolicy:
  - \--out-policy-file is now \--policy.
  - \--policy-digest-alg is now \--policy-algorithm.
  - \--auth-policy-session is now \--policy-session.
  - -L becomes -l.
  - -F becomes -f.
  - -f becomes -o.
  - Removed option \--set-list with short option -L.
  - Removed option \--pcr-input-file with short option -F.
  - Pcr policy options replaced with pcr password mini language.
  - Removed short option a for specifying auth session. Use long option \--policy-session.
  - Removed short option -P for specifying pcr policy. Use long option \--policy-pcr.

* tpm2_createprimary:
  - \--object-attributes is now \--attributes.
  - -o is now -c
  - \--pwdp is now \--hierarchy-auth.
  - \--pwdk is now \--key-auth.
  - \--halg is now \--hash-algorithm.
  - \--kalg is now \--key-algorithm.
  - \--context-object is now \--key-context.
  - \--policy-file is now \--policy.
  - support for unique field when creating objects via -u
  - saves a context file for the generated primary's handle to disk via -c.
  - -A becomes -a.
  - -K becomes -p.
  - -H becomes -C.
  - -g becomes optional.
  - -G becomes optional.

* tpm2_dictionarylockout:
  - \--lockout-passwd is now \--auth.
  - -P becomes -p.

* tpm2_duplicate:
  - New tool for duplicating TPM objects.

* tpm2_encryptdecrypt:
  - \--pwdk is now \--auth.
  - \--out-file is now \--output.
  - -D becomes -d.
  - -I becomes an argument.
  - -P becomes -p.
  - Support IVs via -t or \--iv.
  - Support modes via -G.
  - Support padding via -e or \--pad.
  - Supports input and output to stdin and stdout respectively.

* tpm2_evictcontrol:
  - \--auth is now \--hierarchy.
  - \--context is now \--object-context.
  - \--pwda is now \--auth.
  - \--persistent with short option -S is now an argument.
  - -A becomes -C.
  - Added option \--output -o to serialize handle to disk.
  - Removed option \--handle with short option -H.
  - Raw object-handles and object-contexts are commonly handled with object
    handling logic.
  - Removed option \--input-session-handle with short option -i.
  - Authorization session is now part of password mini language.

* tpm2_getcap:
  - -c becomes an argument.
  - Most instances of value replaced with raw in YAML output.
  - TPM2_PT_MANUFACTURER displays string value and raw value.
  - Supports \--pcr option for listing hash algorithms and bank numbers.

* tpm2_getekcertificate:
  - Renamed from tpm2_getmanufec

* tpm2_getmanufec:
  - Renamed the tool to tpm2_getekcertificate.
  - Removed ek key creation and management logic.
  - Added option for getting ek cert for offline platform via -x.
  - Support for ECC keys.
  - \--ec-cert is now \--ek-certificate,
  - \--untrusted is now \--allow-unverified,
  - \--output is now \--ek-public,
  - -U is now -X.
  - -O is now -x.
  - -f becomes -o.
  - Removed option -P or \--endorse-passwd.
  - Removed option -p or \--ek-passwd.
  - Removed option -w or \--owner-passwd.
  - Removed option -H or \--persistent-handle.
  - Removed option -G or \--key-algorithm.
  - Removed option -N or \--non-persistent.
  - Removed option -O or \--offline.

* tpm2_getpubak:
  - renamed to tpm2_createak.
  - -f becomes -p and -f is used for format of public key output.
  - \--auth-endorse is now \--eh-auth.
  - \--auth-ak is now \--ak-auth.
  - \--halg is now \--hash-algorithm.
  - \--kalg is now \--key-algorithm.
  - -e becomes -P.
  - -P becomes -p.
  - -D becomes -g.
  - -p becomes -u.
  - \--context becomes \--ak-context.
  - \--algorithm becomes \--kalg.
  - \--digest-alg becomes \--halg.
  - \--privfile becomes \--private.
  - remove -k persistant option. Use tpm2_evictcontrol.
  - Fix -o option to -w.
  - now saves a context file for the generated primary's handle to disk.
  - -E becomes -e.
  - -g changes to -G.
  - support for non-persistent AK generation.

* tpm2_getpubek:
  - renamed to tpm2_createek
  - \--endorse-passwd is now \--eh-auth.
  - \--owner-passwd is now \--owner-auth.
  - \--ek-passwd is now \--ek-auth.
  - \--file is now \--public.
  - \--context is now \--ek-context.
  - \--algorithm is now \--key-algorithm.
  - -e is now -P.
  - -P is now -p.
  - -p is now -u.
  - -o is now -w.
  - -g is now -G.
  - Support for saving a context file for the generated primary keys handle
    to disk.
  - support for non-persistent EK generation.
  - -f is now -p.
  - -f support for format of public key output.

* tpm2_getrandom:
  - change default output to binary.
  - add \--hex option for output to hex format.
  - \--out-file is now \--output.
  - bound input request on max hash size per spec, allow -f to override this.

* tpm_gettestresult:
  - new tool for getting test results.

* tpm2_hash:
  - add \--hex for specifying hex output.
  - default output of hash to stdout.
  - default output of hash as binary.
  - remove output of ticket to stdout.
  - \--halg is now \--hash-algorithm.
  - \--out-file is now \--output.
  - -a is now -C.
  - -H is now -a.

* tpm2_hmac:
  - add -t option for specifying ticket result.
  - \--out-file is now \--output.
  - \--auth-key is now \--auth.
  -\--algorithm is now \--hash-algorithm.
  - \--pwdk is now \--auth-key.
  - -C is now -c.
  - -P is now -p.

* tpm2_hierarchycontrol:
  - new tool added for enabling or disabling the use
    of a hierarchy and its associated NV storage.

* tpm2_import:
  - \--object-attributes is now \--attributes.
  - \--auth-parent is now \--parent-auth.
  - \--auth-key is now \--key-auth.
  - \--algorithm is now \--key-algorithm.
  - \--in-file is now \--input.
  - \--parent-key is now \--parent-context.
  - \--privfile is now \--private.
  - \--pubfile is now \--public.
  - \--halg is now \--hash-algorithm.
  - \--policy-file is now \--policy.
  - \--sym-alg-file is now \--encryption-key.
  - -A is now -b.
  - -k is now -i.
  - support OSSL style -passin argument as \--passin for PEM file passwords.
  - support additional import key types:
    - RSA1024/2048.
    - AES128/192/256.
  - -q changes to -u to align with tpm2_loads public/private output arguments.
  - Supports setting object name algorithm via -g.
  - support specifying parent key with a context file.
  - \--parent-key-handle/-H becomes \--parent-key/-C
  - Parent public data option is optional and changes from `-K` to `-U`.
  - Supports importing external RSA 2048 keys via pem files.
  - Supports ECC Parent keys.

* tpm2_incrementalselftest:
  - Add tool to test support of specific algorithms.

* tpm2_listpersistent:
  - deleted as tpm2_getcap and tpm2_readpublic can be used instead.

* tpm2_load:
  - -o is now -c.
  - \--context-parent is now \--parent-context.
  - \--auth-parent is now \--auth.
  - \--pubfile is now \--public.
  - \--privfile is now \--private.
  - \--out-context is now \--key-context.
  - now saves a context file for the generated primary's handle to disk.
  - Option `--pwdp` changes to `--auth-parent`.

* tpm2_loadexternal:
  - \--object-attributes is now --attributes.
  - -o is now -c
  - \--key-alg is now \--key-algorithm.
  - \--pubfile is now \--public.
  - \--privfile is now \--private.
  - \--auth-key is now \--auth.
  - \--policy-file is now \--policy.
  - \--halg is now \--hash-algorithm.
  - \--out-context is now \--key-context.
  - Remove unused -P option.
  - -H is now -a.
  - Fix -A option to -b for attributes.
  - now saves a context file for the generated primary's handle to disk.
  - support OSSL style -passin argument as \--passin for PEM file passwords.
  - name output to file and stdout. Changes YAML stdout output.
  - ECC Public and Private PEM support.
  - AES Public and Private "raw file" support.
  - RSA Public and Private PEM support.
  - Object Attribute support.
  - Object authorization support.
  - Default hierarchy changes to the *null* hierarchy.

* tpm2_makecredential:
  - \--out-file is now \--credential-blob
  - \--enckey is now \--encryption-key.
  - Option `--sec` changes to `--secret`.

* tpm2_nvdefine:
  - \--handle-passwd is now \--hierarchy-auth.
  - \--index-passwd is now \--index-auth.
  - \--policy-file is now \--policy.
  - \--auth-handle is now \--hierarchy.
  - -a becomes -C.
  - -t becomes -a.
  - -I becomes -p.
  - Removed option \--index with short option -x. It is now an argument.
  - Removed option \--input-session-handle with short option -S.
  - Authorization session is now part of password mini language.

* tpm2_nvincrement:
  - New tool to increment value of a Non-Volatile (NV) index setup as a
  counter.

* tpm2_nvlist:
  - tpm2_nvlist is now tpm2_nvreadpublic.

* tpm2_nvread:
  - \--handle-passwd is now \--auth.
  - \--auth-handle is now \--hierarchy.
  - -a becomes -C.
  - Removed option \--index with short option -x. It is now an argument.
  - Removed short option -o for specifying offset. Use long option \--offset.
  - Removed option \--input-session-handle with short option -S.
  - Authorization session is now part of password mini language.
  - Removed option \--set-list with short option -L.
  - Removed option \--pcr-input-file with short option -F.
  - Pcr policy options replaced with pcr password mini language.
  - fix a buffer overflow.

* tpm2_nvreadlock:
  - \--handle-passwd is now \--auth.
  - \--auth-handle is now \--hierarchy.
  - -a becomes -C.
  - Removed option \--index with short option -x. It is now an argument.
  - Removed option \--input-session-handle with short option -S.
  - Authorization session is now part of password mini language.

* tpm2_nvwrite:
  - \--handle-passwd is now \--auth.
  - \--auth-handle is now \--hierarchy.
  - -a becomes -C.
  - Removed option \--index with short option -x. It is now an argument.
  - Removed short option -o for specifying offset. Use long option \--offset.
  - Removed option \--input-session-handle with short option -S.
  - Authorization session is now part of password mini language.
  - Removed option \--set-list with short option -L.
  - Removed option \--pcr-input-file with short option -F.
  - Pcr policy options replaced with pcr password mini language.

* tpm2_nvrelease:
  - \--handle-passwd is now \--auth.
  - \--auth-handle is now \--hierarchy.
  - -a becomes -C.
  - Removed option \--index with short option -x. It is now an argument.
  - Removed option \--input-session-handle with short option -S.
  - Authorization session is now part of password mini language.

* tpm2_nvundefine:
  - Renamed from tpm2_nvrelease.

* tpm2_pcrallocate:
  - New tool for changing the allocated PCRs of a TPM.

* tpm2_pcrevent:
  - \--password is now \--auth.
  - Removed option \--pcr-index with short option -i.
  - PCR index is now specified as an argument.
  - Removed option \--input-session-handle with short option -S.
  - Authorization session is now part of password mini language.

* tpm2_pcrlist:
  - -gls options go away with -g and -l becoming a single argument.

* tpm2_pcrread:
  - Renamed from tpm2_pcrlist.

* tpm2_print:
  - New tool that decodes a TPM data structure and prints enclosed elements
  to stdout as YAML.

* tpm2_policyauthorize:
  - New tool that allows for policies to change by associating the policy to
  a signing authority essentially allowing the auth policy to change.

* tpm2_policycommandcode:
  - New tool to restricts TPM object authorization to specific TPM commands.

* tpm2_policyduplicationselect:
  - New tool for creating a policy to restrict duplication to a new parent
  and or duplicable object.

* tpm2_policylocality:
  - New tool for creating a policy restricted to a locality.

* tpm2_policypcr:
  - New tool to generate a pcr policy event that bounds auth to specific PCR
  values in user defined pcr banks and indices.

* tpm2_policyor:
  - New tool to compound multiple policies in a logical OR fashion to allow
  multiple auth methods using a policy session.

* tpm2_policypassword:
  - New tool to mandate specifying of the object password in clear using a
    policy session.

* tpm2_policysecret:
  - New tool to associate auth of a reference object as the auth of the new
    object using a policy session.

* tpm2_quote:
  - \--ak-context is now \--key-context.
  - \--ak-password is now \--auth.
  - \--sel-list is now \--pcr-list.
  - \--qualify-data is now \--qualification-data.
  - \--pcrs is now \--pcr.
  - \--sig-hash-algorithm is now \--hash-algorithm.
  - -P becomes -p
  - -L becomes -l.
  - -p becomes -o.
  - -G becomes -g.
  - -g becomes optional.
  - Removed option \--id-list with short option -l.
  - Removed option \--ak-handle with short option -k.
  - Raw object-handles and object-contexts are commonly handled with object
    handling logic.

* tpm2_readpublic:
  - \--opu is now \--output.
  - \--context-object is now \--object-context.
  - Removed option \--object with short option -H.
  - Raw object-handles and object-contexts are commonly handled with object
    handling logic.
  - Added \--serialized-handle for saving serialized ESYS_TR handle to disk.
  - Added \--name with short option -n for  saving the binary name.
  - Supports ECC pem and der file generation.

* tpm2_rsadecrypt:
  - \--pwdk is now \--auth.
  - \--out-file is now \--output.
  - -P becomes -p.
  - Added \--label with short option -l for specifying label.
  - Added \--scheme with short option -s for specifying encryption scheme.
  - Removed option -I or in-file input option and make argument.
  - Removed option \--key-handle with short option -k.
  - Raw object-handles and object-contexts are commonly handled with object
    handling logic.
  - Removed option \--input-session-handle with short option -S.
  - Authorization session is now part of password mini language.

* tpm2_rsaencrypt:
  - \--out-file is now \--output.
  - Added \--scheme with short option -s for specifying encryption scheme.
  - Added \--label with -l for specifying label.
  - Removed option \--key-handle with short option -k.
  - Raw object-handles and object-contexts are commonly handled with object
    handling logic.
  - make output binary either stdout or file based on -o.

* tpm2_selftest:
  - New tool for invoking tpm selftest.

* tpm2_send:
  - \--out-file is now \--output.

* tpm2_sign:
  - \--pwdk is now \--auth.
  - \--halg is now \--hash-algorithm.
  - \--sig is now \--signature.
  - -P becomes -p.
  - -s becomes -o.
  - Added \--digest with short option -d.
  - Added \--scheme with short option -s.
  - Supports rsapss.
  - Removed option \--key-handle with short option -k.
  - Raw object-handles and object-contexts are commonly handled with object
    handling logic.
  - Removed option \--msg with short option -m.
  - Make -d toggle if input is a digest.
  - Removed option \--input-session-handle with short option -S.
  - Authorization session is now part of password mini language.
  - Supports signing a pre-computed hash via -d.

* tpm2_startauthsession:
  - New tool to start/save a trial-policy-session (default) or policy-
    authorization-session with command line option --policy-session.

* tpm2_stirrandom:
  - new command for injecting entropy into the TPM.

* tpm2_takeownership:
  - split into tpm2_clear and tpm2_changeauth

* tpm2_testparms:
  - new tool for querying tpm for supported algorithms.

* tpm2_unseal:
  - \--pwdk is now \--auth.
  - \--outfile is now \--output.
  - \--item-context is now \--object-context.
  - -P becomes -p
  - Removed option \--item with short option -H.
  - Raw object-handles and object-contexts are commonly handled with object
    handling logic.
  - Removed option \--input-session-handle with short option -S.
  - Authorization session is now part of password mini language.
  - Removed option \--set-list with short option -L.
  - Removed option \--pcr-input-file with short option -F.
  - Pcr policy options replaced with pcr password mini language.


* tpm2_verifysignature:
  - \--halg is now \--hash-algorithm.
  - \--msg is now \--message.
  - \--sig is now \--signature.
  - -D becomes -d.
  - -t becomes optional.
  - Issue warning when ticket is specified for a NULL hierarchy.
  - Added option \--format with short option -f.
  - Removed option \--raw with short option -r.
  - Removed option \--key-handle with short option -k.
  - Raw object-handles and object-contexts are commonly handled with object
    handling logic.
  - Support routines for OpenSSL compatible format of public keys (PEM, DER) and
    plain signature data without TSS specific headers.

* misc:
  - cmac algorithm support.
  - Add support for reading authorisation passwords from a file.
  - Ported all tools from SAPI to ESAPI.
  - Load TCTI's by SONAME, not raw .so file.
  - system tests are now run with make check when --enable-unit is used in configure.
  - Libre SSL builds fixed.
  - Dynamic TCTIS. Support for pluggable TCTI modules via the -T or --tcti
    options.
  - test: system testing scripts moved into subordinate test directory.
  - configure: enable code coverage option.
  - env: add TPM2TOOLS_ENABLE_ERRATA to control the -Z or errata option.
    affects all tools.
  - Fix parsing bug in PCR mini-language.
  - Fix misspelling of TPM2_PT_HR constants which effects tpm2_getcap output.
  - configure option --with-bashcompdir for specifying bash completion
    directory.

### 3.2.0 - 2019-06-19
  * fix configure bug for linking against libmu.
  * tpm2_changeauth: Support changing platform hierarchy auth.
  * tpm2_flushcontext: Introduce new tool for flushing handles from the TPM.
  * tpm2_checkquote: Introduce new tool for checking validity of quotes.
  * tpm2_quote: Add ability to output PCR values for quotes.
  * tpm2_makecredential: add support for executing tool off-TPM.
  * tpm2_pcrreset: introduce new tool for resetting PCRs.
  * tpm2_quote: Fix AK auth password not being used.

### 3.1.4 - 2019-03-14
  * Fix various man pages
  * tpm2_getmanufec: fix OSSL build warnings
  * Fix broken -T option
  * Various build compatibility fixes
  * Fix some unit tests
  * Update build for recent autoconf-archive versions
  * Install m4 files

### 3.1.3 - 2018-10-15
  * Restore support for the TPM2TOOLS_* env vars for TCTI configuration, in
  addition to supporting the new unified TPM2TOOLS_ENV_TCTI
  * Fix tpm2_getcap to print properties with the TPM_PT prefix, rather than
  TPM2_PT
  * Make test_tpm2_activecredential Python 3 compatible
  * Fix tpm2_takeownership to only attempt to change the specified hierarchies

### 3.1.2 - 2018-08-14
  * Revert the change to use user supplied object attributes exclusively. This is an inappropriate behavioural change for a MINOR version number increment.
  * Fix inclusion of object attribute specifiers section in tpm2_create and tpm2_createprimary man pages.
  * Use better object attribute defaults for authentication, preventing an empty password being used for authentication when a policy is set.

### 3.1.1 - 2018-07-09
  * Allow man page installation without pandoc being available

### 3.1.0 - 2018-06-21
  * Update to use TSS version 2.0
  * When user supplies nv attributes use those exclusively, not in addition to the defaults
  * When user supplies object attributes use those exclusively, not in addition to the defaults
  * Load TCTI's by SONAME, not raw .so file

### 3.0.4 - 2018-05-30
  * Fix save and load for TPM2B_PRIVATE object.
  * Use a default buffer size for tpm2_nv{read,write} if the TPM reports a 0 size.
  * Fix --verbose and --version options crossover.
  * Generate man pages from markdown and include them in the distribution tarball.
  * Print usage summary if tools are executed with no options or man page can't be displayed.

### 3.0.3 - 2017-15-18
  * Tools that don't need a TPM to work no longer request
    a TPM connection. Namely, tpm2_rc_decode
  * Fix undefined references in libmarshal port.

### 3.0.2 - 2017-12-18
  * configure: enable code coverage option.
  * build: enable silent rules options.
  * Add system tests to dist tarball.
  * tpm2_nv(read|write): fix buffer overflows.

### 3.0.1 - 2017-12-11
  * Makefile: add missing LICENSE and markdown files.
### 3.0 - 2017-12-08
  * tpm2_getmanufec: -O as a flag for -f has changed. -O is for existing EK public structure
      and -f is only for generated EK public output.
  * tpm2_nvlist: output in yaml format.
  * tpm2_makecredential format changes to the -o output file.
  * tpm2-quote: -o option removed.
  * tpm2_rsaencrypt: -I is now an argument and input defaults to stdin. -o is optional and
    defaults to stdout.
  * tpm2_listpersistent: output friendly object attributes.
  * tpm2_createprimary: support friendly object attributes via -A. -H becomes auth
    hierarchy.
  * tpm2_create: support friendly object attributes via -A.
  * tpm2_nvwrite and tpm2_nvread have support for satisfying PCR policies.
  * tpm2_encryptdecrypt: has support for EncryptDecrypt2 command.
  * tpm2_nvwrite: -f option removed, support for stdin data supported. Support for starting
      index to write to.
  * errata framework added for dealing with spec errata.
  * tpm2_quote: -G option for signature hash algorithm specification.
  * tpm2_dump_capability: renamed to tpm2_getcap.
  * tpm2_send_command: renamed to tpm2_send and the input file is now an
    argument vs using -i.
  * tpm2_dump_capability: outputs human readable command codes.
  * camelCase options are now all lower case. For example, --camelCase becomes --camel-case.
  * tpm2_quote,readpublic, and sign now have support for pem/der output/inputs. See the
    respective man pages for more details.
  * tpm2_nvread: Has an output file option, -f.
  * manpages: Are now in Markdown and converted to roff using pandoc.
  * tpm2_create - options 'o' and 'O' changed to 'u' and 'r' respectively.
  * tpm2_pcrlist: support yaml output for parsing.
  * tpm2_pcrevent: new tool for hashing and extending pcrs.
  * Make tpm2_{createprimary,create,load,pcrlist,hmac} tools to support the --quiet option.
  * Support for a --quiet option to suppress messages printed by tools to standard output.
  * tpm2_hmac: support for files greater than 1024 bytes, changes in options and arguments.
  * tpm2_hash: support for files greater than 1024 bytes, changes in options and arguments.
  * Install is now to bin vs sbin. Ensure that sbin tools get removed!
  * make dist and distcheck are now working.
  * installation into c
