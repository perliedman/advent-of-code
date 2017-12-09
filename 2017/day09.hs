import Debug.Trace

data Context = Context {
  depth :: Int,
  garbage :: Int
} deriving (Show)

addDepth context v = Context {depth=depth context + v, garbage = garbage context}
addGarbage context = Context {depth=depth context, garbage = garbage context + 1}

-- parseStream (x:xs) context | trace ("parseStream " ++ show x ++ " at context " ++ show context) False = undefined
parseStream [] context = (0, context)
parseStream ('{':xs) context = let
  (score, finalContext) = parseStream xs (addDepth context 1)
  in (depth context + 1 + score, finalContext)
parseStream ('}':xs) context = parseStream xs (addDepth context (-1))
parseStream ('<':xs) context = parseGarbage xs context
parseStream ('!':xs) context = ignoreOne xs context parseStream
parseStream (',':xs) context = parseStream xs context
parseStream ('\n':xs) context = parseStream xs context

ignoreOne (_:xs) context next = next xs context

parseGarbage ('>':xs) context = parseStream xs context
parseGarbage ('!':xs) context = ignoreOne xs context parseGarbage
parseGarbage (_:xs) context = parseGarbage xs (addGarbage context)

main = do
  contents <- getContents
  putStr (show $ parseStream contents (Context {depth=0, garbage=0}))
  putStr ("\n")
