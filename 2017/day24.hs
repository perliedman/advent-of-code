import Data.List
import Data.List.Split
import Data.Ord
import qualified Data.Set as Set

matchesPort :: Int -> (Int, Int) -> Bool
matchesPort x (a, b) = a == x || b == x

findMatching :: Set.Set (Int, Int) -> Int -> Set.Set (Int, Int)
findMatching ps x = Set.filter (matchesPort x) ps

-- findMaxBridge :: Set.Set (Int, Int) -> Int -> (Int, [(Int, Int)])
findMaxBridge best ps x
  | ps == Set.empty = (0, [])
  | otherwise = Set.foldl' (\bestYet p -> best bestYet (findBest p)) (0, []) (findMatching ps x)
  where 
    findBest p = (ap + bp + bestStrength, p:bestBridge)
      where 
        (ap, bp) = p
        (bestStrength, bestBridge) = findMaxBridge best (Set.delete p ps) (otherPort p x)
        otherPort (a, b) x = if a == x then b else a

bestPair (as, ab) (bs, bb) = if as > bs then (as, ab) else (bs, bb)
longestPair (as, ab) (bs, bb)
  | length ab > length bb = (as, ab)
  | length bb > length ab = (bs, bb)
  | as > bs = (as, ab)
  | otherwise = (bs, bb)

parse = pair . map (\x -> read x :: Int) . splitOn "/"
  where pair [a, b] = (a, b)

main = do
  contents <- getContents
  -- putStr (show $ findMaxBridge bestPair (Set.fromList $ map parse $ lines contents) 0)
  putStr (show $ findMaxBridge longestPair (Set.fromList $ map parse $ lines contents) 0)
