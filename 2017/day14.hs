import KnotHash
import Data.List.Split
import Data.Char
import Numeric
import Data.Bits
import Data.Array
import qualified Graphics.Image as I

countHashBits = sum . map ((\x -> popCount (x :: Integer)) . fst . head . readHex)
knotHashes i = map (\x -> hash $ i ++ "-" ++ (show x)) [0..127]

a = countHashBits . knotHashes

nibbleToBits x = let
  toInt False = 0 :: Int
  toInt True = 1 :: Int
  f x n = if n >= 0 then (toInt $ testBitDefault x n):(f x (n-1)) else []
  in f x 3

digitsToBits = map ((\x -> nibbleToBits (x :: Int)) . fromIntegral . fst . head . readHex)
hexStrToDigits = filter (\x -> x /= "") . splitOn ""
hexStrToBits = concat . digitsToBits . hexStrToDigits
hashesToBits = map hexStrToBits

toComplexArray :: [[a]] -> Array(Int, Int) a
toComplexArray grid = array ((0,0),((length $ grid !! 0) - 1,(length grid) - 1))  entries  
  where entries = concatMap (\z -> map (\y -> ((fst y, fst z), snd y))  (snd z)) $ zip [0..] $ map (\x -> zip [0..] x) grid

inBounds :: Array (Int, Int) Int -> (Int, Int) -> Bool
inBounds grid (x, y) = x >= lowx && x <= highx && y >= lowy && y <= highy
  where ((lowx, lowy), (highx, highy)) =  bounds grid
 
replace :: Array (Int, Int) Int -> (Int, Int) -> Int -> Array (Int, Int) Int
replace grid point replacement = if inBounds grid point then grid // [(point, replacement)] else grid
floodFill :: Array (Int, Int) Int ->  (Int, Int) -> Int -> Int -> Array (Int, Int) Int
floodFill grid point@(x, y) target replacement =
  if((not $ inBounds grid point) ||  grid ! (x,y) /= target) then grid 
  else 
    gridNorth
    where grid' = replace grid point replacement
          gridEast = floodFill grid' (x+1, y) target replacement
          gridWest = floodFill gridEast (x-1, y) target replacement
          gridSouth = floodFill gridWest (x, y+1) target replacement
          gridNorth = floodFill gridSouth (x, y-1) target replacement

fillGroups grid = let
  ((_, _), (w, h)) = bounds grid
  fillGroup grid (x, y) gn = let
    v = grid ! (x, y)
    nextC = if x < w then (x+1, y) else (0, y+1)
    filled = if v == 1 then floodFill grid (x, y) 1 gn else grid
    in if y<=h then fillGroup filled nextC (if v == 1 then gn+1 else gn) else (grid, gn)
  (filledGrid, ngroups) = fillGroup grid (0, 0) 2
  in (filledGrid, ngroups - 2)

b = snd . fillGroups . toComplexArray . hashesToBits . knotHashes

gridToPixel grid c = let
  t = (grid ! c)
  in (I.PixelRGB ((fromIntegral ((t `mod` 7) * 20)) :: Double) (fromIntegral (t `mod` 5) * 20) (fromIntegral (t `mod` 11) * 20)) / 200

makeImage grid = I.makeImageR I.VU (128, 128) (gridToPixel grid)

bImage = makeImage . fst . fillGroups . toComplexArray . hashesToBits . knotHashes

main = do
  I.writeImage "day14.png" $ bImage "uugsqrei"
