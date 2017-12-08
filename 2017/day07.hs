import qualified Text.Regex as Re
import Data.List.Split
import Data.Maybe
import qualified Data.Map.Strict as Map
import Debug.Trace

data Tower a b = Program a b | Disc a b [Tower a b] | Tbd a deriving (Show, Eq, Ord)

towerName (Program a _) = a
towerName (Disc a _ _) = a
towerName (Tbd a) = a

-- addTower :: Eq a => (Tower a b) -> a -> (Tower a b) -> (Tower a b)
-- addTower t parentName (Program name w) = if name == parentName then Disc parentName w [t] else Program name w
-- addTower t parentName (Disc name w children) = let
--   removeTbd name xs = [c | c <- xs, towerName c /= name]
--   in if name == parentName then Disc parentName w (t:removeTbd name children) else Disc name w (map (addTower t parentName) children)

containsTbd x (Program name _) = False
containsTbd x (Tbd name) = return x == name
containsTbd x (Disc name _ children) = return x == name || any (containsTbd x) children

replaceTbd :: Eq a => (Tower a b) -> a -> (Tower a b) -> (Tower a b)
replaceTbd t parentName (Program name w) = if name == parentName then Disc parentName w [t] else Program name w
replaceTbd t parentName (Disc name w children) = let
  removeTbd name xs = [c | c <- xs, towerName c /= name]
  in if name == parentName then Disc parentName w (t:removeTbd name children) else Disc name w (map (replaceTbd t parentName) children)

-- removeTbds ((name, t):ts) 

buildTower [] parts = parts
buildTower ((name, weight, []):defs) parts = buildTower defs (Map.insert name (Program name weight) parts)
buildTower ((name, weight, children):defs) parts = let
  makeChild name Nothing = Tbd name
  makeChild _ (Just t) = t
  childTowers = map (\x -> (makeChild x) $ Map.lookup x parts) children
  nextParts = foldl (\m x -> Map.delete x m) parts children
  in buildTower defs (Map.insert name (Disc name weight childTowers) nextParts)

--towerName (Tower a b) = a

-- tower input = let
--   parsedLines = parseInput input
--   in buildTower (namedChildren parsedLines) (programMap $ namedPrograms parsedLines)

-- buildTower :: (Ord a) => (Show a) => (Show b) => [(a, [a])] -> Map.Map a (Tower a b) -> (Tower a b)
-- buildTower [] programMap = snd $ head $ Map.toList programMap
-- buildTower ((name, children):ps) programMap | trace ("buildTower (" ++ show name ++ ", " ++ show children ++ ") " ++ show programMap) False = undefined
-- buildTower ((name, children):ps) programMap = let
--   Just program = Map.lookup name programMap
--   childPrograms = catMaybes $ map (\name -> Map.lookup name programMap) children
--   createSubTower a [] = a
--   createSubTower (Program a b) children = Disc a b children
--   in buildTower ps (Map.insert name (createSubTower program childPrograms) (removeProgramsFromMap children programMap))



-- getTower sname towerMap ((pname, children):defs) = let
--   tower (Just t) = (t, towerMap)
--   tower Nothing = buildTower sname towerMap defs
--   in 


-- removeProgramsFromMap [] map = map
-- removeProgramsFromMap (x:xs) map = removeProgramsFromMap xs (Map.delete x map)

-- namedChildren ps = let
--   parseChildren children = filter (not . null) $ splitOn ", " children
--   programChildren [_, _, _, children] = children
--   in zip (map programName ps) (map (parseChildren . programChildren) ps)

-- namedPrograms ps = zip (map programName ps) (map buildProgram ps)
-- programMap namedPrograms = Map.fromList namedPrograms
-- buildProgram [name, weight, _, _] = Program name (parseWeight weight)
-- parseWeight x = read x :: Int
-- programName [name, _, _, _] = name

definitions input = let
  parseChildren children = filter (not . null) $ splitOn ", " children
  f [name, weight, _, childStr] = (name, read weight :: Int, parseChildren childStr)
  in map f input

lineExp = Re.mkRegex "^([a-z]+) \\(([0-9]+)\\)( -> (.*)|)$"
parseInput input = catMaybes $ map (Re.matchRegex lineExp) $ lines input

main = do
  contents <- getContents
  putStr (show $ buildTower (definitions $ parseInput contents) Map.empty)
  -- putStr (show $ tower contents)
  putStr "\n"