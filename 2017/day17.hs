import Debug.Trace
import Data.List.Split
import Data.Maybe

insertAt xs n new_element = let
  (ys,zs) = splitAt n xs
  in ys ++ [new_element] ++ zs

nextIndex step l cp = (cp + step) `mod` l

spinLock step n = let
  spin v i xs = let
    nv = v+1
    ni = nextIndex step nv i
    in if v <= n then
      spin nv (ni+1) (insertAt xs (ni + 1) nv)
    else
      xs
  in spin 0 0 [0]

a x = head $ head $ tail $ splitOn [2017] (spinLock x 2017)

-- spinFind step n x = let
--   spin v i r = let
--     nv = v+1
--     ni = nextIndex step nv i
--     in if v <= n then
--       spin nv (ni+1) (if ni == x then (Just nv) else r)
--     else
--       r
--   in spin 0 0 Nothing

spinFind step n x = let
  spin v i r
      | v > n = r
      | ni == x = spin nv (ni+1) (Just nv)
      | otherwise = spin nv (ni+1) r
    where
      nv = v+1
      ni = nextIndex step nv i
  in spin 0 0 Nothing

main = do
  putStr (show $ spinFind 303 50000000 0)
  putStr ("\n")
