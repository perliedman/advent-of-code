import Debug.Trace

-- revcycle len l skip xs | trace ("revcycle " ++ 
--   " h=" ++ show (take (len+skip) xs) ++
--   " t=" ++ show (reverse $ take l xs) ++
--   " =>" ++ show ((take len xs) ++ (reverse $ take l xs))) False = undefined
revcycle len l skip xs = let
  h = take len xs
  t = reverse $ take l xs
  in drop skip $ cycle $ drop l (h ++ t)

pinchtwist :: Int -> ([Int], Int, Int) -> [Int] -> ([Int], Int, Int)
-- pinchtwist len (xs, p, skip) (l:ls) | trace ("pinchtwist " ++ 
--   show len ++ " " ++ show p ++ " " ++ show skip ++
--   " h=" ++ show (take (len+skip) xs) ++
--   " t=" ++ show (reverse $ take l xs) ++
--   " =>" ++ show ((take (len+skip) xs) ++ (reverse $ take l xs))) False = undefined
-- pinchtwist len (xs, p, skip) [] | trace ("pinchtwist " ++ show len ++ " " ++ show p ++ " " ++ show skip) False = undefined
pinchtwist len (xs, p, skip) [] = (take len $ drop (len - (p `mod` len)) xs, p, skip)
pinchtwist len (xs, p, skip) (l:ls) = let
  in pinchtwist len (revcycle len l skip xs, p + l + skip, skip + 1) ls

stdsuffix = [17, 31, 73, 47, 23]
