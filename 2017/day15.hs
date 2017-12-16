import Data.Bits
import Data.List

gen factor p = (p * factor) `mod` 2147483647

genDiv gen d p = let
  v = gen p
  in if v `mod` d == 0 then v else genDiv gen d v

genA = gen 16807
genB = gen 48271

genDivA = genDiv genA 4
genDivB = genDiv genB 8

-- genSeq gen seed = foldl' (\xs _ -> (gen $ head xs):xs) [seed]

-- sA seed = genSeq genA seed
-- sB seed = genSeq genB seed

-- a seedA seedB = length $ filter (\(x,y) -> x == y) $ zip (sA seedA [1..40000000]) (sB seedB [1..40000000])

findEquals seedA seedB fa fb n = go 0 seedA seedB 1
  where
    go :: Integer -> Integer -> Integer -> Integer -> Integer
    go eqs a b count
        | count >= n = eqs
        | ga .&. 65535 == gb .&. 65535   = go (eqs + 1) ga gb (count+1)
        | otherwise      = go eqs ga gb (count+1)
      where
        ga = fa a
        gb = fb b

main = do
  -- putStr (show $ findEquals 703 516 genA genB 40000000)
  putStr (show $ findEquals 703 516 genDivA genDivB 5000000)
  putStr ("\n")
