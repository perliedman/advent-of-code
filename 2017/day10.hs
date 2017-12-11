import Debug.Trace
import Data.Char
import Data.Bits
import Data.List.Split
import Numeric

revcycle len l skip xs = let
  h = take len xs
  t = reverse $ take l xs
  in drop skip $ cycle $ drop l (h ++ t)

pinchtwist :: Int -> ([Int], Int, Int) -> [Int] -> ([Int], Int, Int)
pinchtwist len (xs, p, skip) [] = (take len $ drop (len - (p `mod` len)) xs, p, skip)
pinchtwist len (xs, p, skip) (l:ls) = let
  in pinchtwist len (revcycle len l skip xs, p + l + skip, skip + 1) ls

stdsuffix = [17, 31, 73, 47, 23]

sparseHash l = let
  (h, _, _) = foldl (\(xs, p, skip) _ -> pinchtwist 256 (drop p $ cycle xs, p, skip) l) ([0..255], 0, 0) [1..64]
  in h

strToLengths s = map ord s ++ stdsuffix

denseHash :: [Int] -> [Int]
denseHash xs = let
  xorGroup gs = foldl1 (\a x -> a `xor` x) gs
  in map xorGroup $ chunksOf 16 xs

toHexStr xs = concat $ map (\x -> if x < 16 then "0" ++ showHex x "" else showHex x "") xs

hash :: String -> String
hash = toHexStr . denseHash . sparseHash . strToLengths
