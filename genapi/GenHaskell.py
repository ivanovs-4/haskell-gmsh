# This is a heavily adopted version of the Gmsh API generation file
# for the purpose of generating Haskell c2hs definitions from the
# Gmsh API definitions file:
# https://gitlab.onelab.info/gmsh/gmsh/blob/master/api/gen.py

# Original file can be found from:
# https://gitlab.onelab.info/gmsh/gmsh/blob/master/api/GenApi.py

# Credit to
# Gmsh - Copyright (C) 1997-2019 C. Geuzaine, J.-F. Remacle
# Contributor(s):
#   Jonathan Lambrechts

#
# Modifications for Haskell by Antero Marjamäki (first.last@tuni.fi)
#



class arg:
    output = False
    def __init__(self, name=None, value=None,  python_value=None, julia_value=None):
        self.name = name
        self.value = value

    def foreignexp(self):
        return [self.ctype]

    def type_signature(self):
        return [self.htype]

    def ccall_inputs(self):
        return "{}'".format(self.name)

class oarg(arg):
    output = True
    def foreignexp(self):
        # these things are either the return values of the C function
        # or ordinary "reference" variables
        return ["Ptr {}".format(self.ctype)]

    def type_signature(self):
        return [self.htype]

    def type_in_return(self):
        return [self.ctype]



# these things are not given as return values from the C api,
# because that's impossible
class input_array(arg):
    def foreignexp(self):
        out = ["Ptr {}".format(self.ctype), "CInt"]
        return out

    def ccall_inputs(self):
        n = self.name
        return "{}' {}'_n".format(n, n)

class input_arrayarray(arg):
    def foreignexp(self):
        out = ["Ptr (Ptr {})".format(self.ctype), "Ptr CInt", "CInt"]
        return out

    def ccall_inputs(self):
        n = self.name
        return "{}' {}'_n {}'_nn".format(n,n,n)

class output_array(oarg):
    def foreignexp(self):
        return ["Ptr ( Ptr {})".format(self.ctype),
                "Ptr CInt"]

    def ccall_inputs(self):
        n = self.name
        return "{}' {}'_n".format(n, n)

class output_arrayarray(oarg):
    def foreignexp(self):
        return ["Ptr (Ptr (Ptr {}))".format(self.ctype),
                "Ptr (Ptr CInt)",
                "Ptr CInt"]

    def ccall_inputs(self):
        n = self.name
        return "{}' {}'_n {}'_nn".format(n,n,n)

# input types
class ibool(arg):
    htype = "Bool"
    ctype = "CBool"

    def marshall_in(self):
        return ["let {}' = fromBool {}".format(self.name, self.name)]


class iint(arg):
    htype = "Int"
    ctype = "CInt"

    def marshall_in(self):
        return ["let {}' = fromIntegral {}".format(self.name, self.name)]

class isize(arg):
    htype = "Int"
    ctype = "CInt"

    def marshall_in(self):
        return ["let {}' = fromIntegral {}".format(self.name, self.name)]

class idouble(arg):
    htype = "Double"
    ctype = "CDouble"

    def marshall_in(self):
        return ["let {}' = fromReal {}".format(self.name, self.name)]

class istring(arg):
    htype = "String"
    ctype = "CString"

    def marshall_in(self):
        return ["withCString {} $ \\{}' -> do".format(self.name, self.name)]

class ivoidstar(arg):
    htype = "?"
    ctype = "?"

    def marshall_in(self):
        return ["?"]

class ivectorint(input_array):
    htype = "[Int]"
    ctype = "CInt"

    def marshall_in(self):
        return ["withArrayLen $ \\{}' {}'_n -> do".format(self.name, self.name)]

class ivectorsize(input_array):
    htype = "[Int]"
    ctype = "CInt"

    def marshall_in(self):
        return ["withArrayLen $ \\{}' {}'_n -> do".format(self.name, self.name)]

class ivectordouble(input_array):
    htype = "[Double]"
    ctype = "Double"

    def marshall_in(self):
        return ["withArrayLen $ \\{}' {}'_n -> do".format(self.name, self.name)]

class ivectorstring(input_array):
    htype = "[String]"
    ctype = "CString"

    def marshall_in(self):
        return ["?"]

class ivectorpair(input_array):
    htype = "[(Int, Int)]"
    ctype = "CInt"

    def marshall_in(self):
        return ["withArrayLen $ \\{}' {}'_n -> do".format(self.name, self.name)]


# seems like not in use
# class ivectorvectorint(arg):
#     htype = ""
#     ctype = ""

class ivectorvectorsize(input_arrayarray):
    htype = "[[Int]]"
    ctype = "CInt"

    def marshall_in(self):
        return ["withArrayLen $ \\{}' {}'_n -> do".format(self.name, self.name)]


class ivectorvectordouble(input_arrayarray):
    htype = "[[Double]]"
    ctype = "CDouble"

    def marshall_in(self):
        n = self.name
        return ["withArrayArrayLen $ \\{}' {}'_n {}'_nn -> do".format(n,n,n)]


# output types

class oint(oarg):
    htype = "Int"
    ctype = "CInt"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n)]


class osize(oarg):
    htype = "Int"
    ctype = "CInt"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n)]

class odouble(oarg):
    htype = "Double"
    ctype = "CDouble"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n)]

class ostring(oarg):
    htype = "String"
    ctype = "CString"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n)]

class ovectorint(output_array):
    htype = "[Int]"
    ctype = "CInt"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n),
                "alloca $ \\{}_n -> do".format(n)]

class ovectorsize(output_array):
    htype = "[Int]"
    ctype = "CInt"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n),
                "alloca $ \\{}_n -> do".format(n)]

class ovectordouble(output_array):
    htype = "[Double]"
    ctype = "CDouble"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n),
                "alloca $ \\{}_n -> do".format(n)]

class ovectorstring(output_array):
    htype = "[String]"
    ctype = "CString"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n),
                "alloca $ \\{}_n -> do".format(n)]

class ovectorpair(output_array):
    htype = "Int"
    ctype = "CInt"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n),
                "alloca $ \\{}_n -> do".format(n)]


# Not used
# class ovectorvectorint(ivectorvectorint):
#     output = True

class ovectorvectorsize(output_arrayarray):
    output = True
    htype = "[[Int]]"
    ctype = "CInt"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n),
                "alloca $ \\{}_n -> do".format(n),
                "alloca $ \\{}_nn -> do".format(n)]

class ovectorvectordouble(output_arrayarray):
    output = True
    htype = "[[Double]]"
    ctype = "CDouble"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n),
                "alloca $ \\{}_n -> do".format(n),
                "alloca $ \\{}_nn -> do".format(n)]

class ovectorvectorpair(output_arrayarray):
    output = True
    htype = "[[(Int, Int)]]"
    ctype = "CInt"

    def marshall_in(self):
        n = self.name
        return ["alloca $ \\{} -> do".format(n),
                "alloca $ \\{}_n -> do".format(n),
                "alloca $ \\{}_nn -> do".format(n)]

class argcargv(arg):
    output = False
    def __init__(self, *args):
        self.name = "argv"
        self.htype = None
        self.ctype = None

    def marshall_in(self):
        n = self.name
        return ["let argc' = length argv",
                "withArgv argv $ \\argv' -> do"]

    def foreignexp(self):
        return ["CInt", "Ptr CString"]

    def type_signature(self):
        return ["[String]"]

    def ccall_inputs(self):
        return "argc' argv'"

def camelcasify(str):
    """ raise the first letter to uppercase """
    return str[0].upper() + str[1:]

def flatten2(lst):
    return [x for xs in lst for x in xs]

class Function:
    def __init__(self, rtype, name, args, doc, special=[]):
        self.return_type = rtype
        self.name = name
        self.args = args
        self.doc = doc
        self.special = special

    def to_string(self, prefix):
        return "\n".join([self.str_type_signature(prefix),
                          self.str_body(prefix),
                          self.str_foreignexp(prefix)])

    def input_arguments(self):
        return [a for a in self.args if not a.output]

    def output_arguments(self):
        return [x for x in self.args if x.output]

    def str_type_signature(self, prefix):
        """ Generate the type signature for the haskell function
        Input variables need to be present, output variables are wrapped
        in the IO action.

        If function has the return_type specified, it will always be the first
        one in IO(...)

        Example:

        gmshModelGetEntities :: Int -> IO([(Int, Int)]) """

        fname = prefix  + camelcasify(self.name)
        inputs = self.input_arguments()
        outputs = self.output_arguments()
        if self.return_type is not None:
            outputs = [self.return_type] + outputs

        itypes = flatten2([a.type_signature() for a in inputs])
        itypesign = " -> ".join(itypes)

        if(len(itypesign) > 0):
            itypesign += " -> "

        otypes = flatten2([a.type_signature() for a in outputs])
        otypesign = ", ".join(otypes)

        return "".join([fname, " :: ",  itypesign, "IO(", otypesign, ")"])

    def str_body(self, prefix):
        """ Generates the body of the function call with marshalling etc.

        some sort of template:

        fname i1 i2 ... in = do
            let ik1 = ...
            ... types which can be converted to C values ...

            withArrayLen $ \ arr1 arr1_n ->
            ... all input types which are delivered using pointers

            alloca $ \ o1 -> do
            ... return types which need allocation

            alloca $ \ errptr -> do
            ... the error pointer

            -- the actual call to the function
            out = cfname ...arguments...

            checkErrorCodeAndThrow errptr

            -- output marshalling
            oval <- out
            let moval = marshaller oval

            -- peeking and marshalling output arguments
            oval1 <- peekX o1
            ...

            -- the actual output argument always first
            return (moval, oval1, oval2, ... ovaln)

        """

        inputs = self.input_arguments()
        outputs = self.output_arguments()
        rtype = self.return_type
        fname = prefix + camelcasify(self.name)

        ## Function declaration line
        decline = [fname]
        for a in inputs:
            decline.append(a.name)
        decline.append("= do")
        lines = [" ".join(decline)]

        ## Input variables with marshalling
        for a in inputs:
            for l in a.marshall_in():
                lines.append("   "+l)

        ## Output variables with marshalling
        for a in outputs:
            for l in a.marshall_in():
                lines.append("   "+l)

        ## error ptr
        lines.append("   alloca $ \\errptr -> do")

        ## the actual call
        if rtype is None:
            calline = ["   c{}".format(fname)]
        else:
            calline = ["   {} <- c{}".format(rtype.name, fname)]
        for a in inputs:
            calline.append(a.ccall_inputs())
        # error pointer to the end
        calline.append("errptr")
        lines.append(" ".join(calline))

        ## check error code
        lines.append("   checkErrorCodeAndThrow errptr")

        ## output marshalling
        ## TODO: continue from here!
        #if rtype is not None:
            #lines.append("   let {}' = {}".format(rtype.name, rtype.name))
            #lines.append(rtype.marshall_out())
        lines.append("   return ()")


        return "\n".join(lines)

    def str_foreignexp(self, prefix):
        """
        Generates the foreign import statement for the function, as a string.

        Example:

        foreign import ccall unsafe "gmshc.h gmshModelGetEntities"
         cgmshModelGetEntities
            :: Ptr (Ptr CInt)
            -> Ptr CInt
            -> CInt
            -> Ptr CInt
            -> IO()

        """
        """ ATTENTION: the vector sizes are not present in the
        api_gen.py. Probably need to refactor this to
        the argument class (argument class needs to create
        a string for itself, only it knows when extra sizes are present
        in the c call.) """

        fname = prefix + camelcasify(self.name)
        lines = ["foreign import ccall unsafe \"gmshc.h {}\"".format(fname)]
        lines.append("   {}".format("c"+fname))

        # print arguments (c types), always at least errorcode
        # which is not present in the api definition
        args = list(self.args) + [oint("errcode")]
        types = flatten2([a.foreignexp() for a in args])

        lines.append("      :: {}".format(types[0]))
        for t in types[1:]:
            lines.append("      -> {}".format(t))

        if self.return_type is None:
            lines.append("      -> IO()")
        else:
            t = self.return_type.type_in_return()[0]
            lines.append("      -> IO({})".format(t))

        return "\n".join(lines)

class Module:

    def __init__(self, name, doc):
        self.name = name
        self.doc = doc
        self.fs = []
        self.submodules = []

    def add(self, name, doc, rtype, *args):
        # let's name the output variable oval to ease the process
        if rtype is not None:
            rtype = rtype("oval")
        self.fs.append(Function(rtype, name, args, doc, []))

    def add_special(self, name, doc, special, rtype, *args):
        if rtype is not None:
            rtype = rtype("oval")
        self.fs.append(Function(rtype, name, args, doc, special))

    def add_module(self, name, doc):
        module = Module(name, doc)
        self.submodules.append(module)
        return module

    def write_module(self, fhandle, **kwargs):
        fwd_kwargs = kwargs.copy()
        kwprefix = kwargs.get('prefix', None)

        if kwprefix is None:
            prefix = self.name
            fwd_kwargs['prefix'] = prefix
        else:
            prefix = kwprefix+camelcasify(self.name)
            fwd_kwargs['prefix'] = prefix

        #fhandle.write("Module {}: \n".format(prefix))
        # take only one function from each module at first
        for f in self.fs[0:1]:
            fhandle.write(f.to_string(prefix))
            fhandle.write("\n")

        for m in self.submodules[0:1]:
            m.write_module(fhandle, **fwd_kwargs)



class API:

    def __init__(self, version_major, version_minor, namespace="gmsh", code="Gmsh",
                 copyright="Gmsh - Copyright (C) 1997-2019 C. Geuzaine, J.-F. Remacle",
                 issues="https://gitlab.onelab.info/gmsh/gmsh/issues."):
        self.version_major = version_major
        self.version_minor = version_minor
        global ns
        ns = namespace
        self.code = code
        self.copyright = copyright
        self.issues = issues
        self.modules = []

    def add_module(self, name, doc):
        module = Module(name, doc)
        self.modules.append(module)
        return module

    def write_julia(self):
        pass

    def write_texi(self):
        pass

    def write_cpp(self):
        pass

    def write_c(self):
        pass

    def write_python(self):
        """ Just kidding! Write Haskell instead! """

        with open("GmshAPI.hs", 'w') as f:
            f.write(haskell_header)
            for m in self.modules[0:1]:
                m.write_module(f)


haskell_header = """
{-
GmshAPI.chs - c2hs definitions of the GMSH C API.
Copyright (C) 2019  Antero Marjamäki

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License ("LICENSE" file) for more details.
-}

module GmshAPI where

import Control.Monad (liftM)
import Control.Applicative ((<$>))
import Foreign.C -- get the C types
import Foreign.Ptr (Ptr,nullPtr)
import Foreign.C.String (withCString)
import Foreign.Marshal (alloca)
import Foreign.Marshal.Utils (withMany)
import Foreign.Marshal.Array (withArray, peekArray, advancePtr, withArrayLen)
import Foreign.Storable (peek, Storable)
import Data.Maybe (fromMaybe)
import Debug.Trace (trace)

--import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as V


--include "gmshc.h"

toInt :: Ptr CInt -> IO Int
toInt = liftM fromIntegral . peek

-- marshaller for argv type "char ** argv"
withArgv :: [String] -> (Ptr CString -> IO a) -> IO a
withArgv ss f = withMany withCString ss f'
   where
      f' x = withArray x f

peekInt :: Ptr CInt -> IO(Int)
peekInt = liftM fromIntegral . peek


flatToPairs :: [a] -> [(a,a)]
flatToPairs [] = []
flatToPairs (x:y:[]) = [(x,y)]
flatToPairs (x:y:xs) = (x,y) : flatToPairs xs

pairsToFlat :: [(a,a)] -> [a]
pairsToFlat lst = reverse $ foldl (\\acc (a,b) -> b:a:acc) [] lst


-- Ptr (Ptr CInt) is a serialized list of integers, i.e.
-- **int is a pointer to an array, not an array of arrays... D'OH!
peekArrayPairs :: Ptr CInt -> Ptr (Ptr CInt) -> IO([(Int, Int)])
peekArrayPairs nptr arrptr  = do
  npairs <- peekInt nptr
  arr <- peek arrptr
  flatpairs <- peekArray npairs arr
  return $ flatToPairs $ map fromIntegral flatpairs

--foldfun :: ([[(CInt, CInt)]], Ptr (Ptr CInt))
-- -> Int -> IO([[(CInt, CInt)]], Ptr (Ptr CInt))

peekArrayArrayPairs
  :: Ptr CInt
  -> Ptr (Ptr CInt)
  -> Ptr (Ptr (Ptr CInt))
  -> IO([[(Int, Int)]])
peekArrayArrayPairs lengthLengthsPtr lengthsPtr arrPtr  =
  do
    nlengths <- peekInt lengthLengthsPtr
    lengthsArr <- peek lengthsPtr
    lengthsList <- peekArray nlengths lengthsArr
    arrptr <- peek arrPtr
    -- okay, so. fold over lengthsList.
    -- For each element dereference the pointer
    -- then peek n elements from the array, then advance the outer pointer
    -- accumulate the list of peeked lists, and the advanced pointer
    (pairs,_) <- foldl foldfun (return ([], arrptr)) $ map fromIntegral lengthsList
    return pairs

  where
    -- foldfun takes the previous IO action and runs it,
    -- then proceeds to peek and advance ptrs and wraps the results
    -- in a tuple
    foldfun action n = do
        (acc, ptr) <- action
        aptr <- peek ptr
        lst <- peekArray n aptr
        let pairss = flatToPairs $ map fromIntegral lst
        let newptr = advancePtr ptr 1
        return ((pairss:acc), newptr)



checkErrorCodeAndThrow :: String -> Ptr CInt -> IO()
checkErrorCodeAndThrow funname errptr = do
  errcode <- peekInt errptr
  if errcode == 0
      then return ()
      else error $ funname ++ " returned nonzero error code: " ++ show errcode

"""
