import Debug.Trace

-- parseStream (x:xs) depth | trace ("parseStream " ++ show x ++ " at depth " ++ show depth) False = undefined
parseStream [] _ = 0
parseStream ('{':xs) depth = (depth+1) + (parseStream xs (depth + 1))
parseStream ('}':xs) depth = parseStream xs (depth - 1)
parseStream ('<':xs) depth = parseGarbage xs depth
parseStream ('!':xs) depth = ignoreOne xs depth parseStream
parseStream (',':xs) depth = parseStream xs depth
parseStream ('\n':xs) depth = parseStream xs depth

ignoreOne (_:xs) depth next = next xs depth

parseGarbage ('>':xs) depth = parseStream xs depth
parseGarbage ('!':xs) depth = ignoreOne xs depth parseGarbage
parseGarbage (_:xs) depth = parseGarbage xs depth

main = do
  contents <- getContents
  putStr (show $ parseStream contents 0)
  putStr ("\n")
