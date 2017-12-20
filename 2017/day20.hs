import qualified Text.Regex as Re
import Data.Maybe
import Data.List

data Vec3 = Vec3 { x :: Int, y :: Int, z :: Int } deriving (Eq, Show, Read)
type Particle = (Vec3, Vec3, Vec3)

vadd (Vec3 {x=x1, y=y1, z=z1}) (Vec3 {x=x2, y=y2, z=z2}) = Vec3 {x=x1+x2, y=y1+y2, z=z1+z2}

vabs (Vec3 {x=x, y=y, z=z}) = abs x + abs y + abs z 

parseInput input = let
  lineExp = Re.mkRegex "^p=<(-*[0-9]+),(-*[0-9]+),(-*[0-9]+)>, v=<(-*[0-9]+),(-*[0-9]+),(-*[0-9]+)>, a=<(-*[0-9]+),(-*[0-9]+),(-*[0-9]+)>$"
  f [px, py, pz, vx, vy, vz, ax, ay, az] = (Vec3{x=px,y=py,z=pz}, Vec3{x=vx,y=vy,z=vz}, Vec3{x=ax,y=ay,z=az})
  in map (f . map (\x -> read x :: Int)) $ catMaybes $ map (Re.matchRegex lineExp) $ lines input

minAcc :: [(Int, Vec3)] -> Maybe (Int, Vec3)
minAcc ps = let
  cmp :: Maybe (Int, Vec3) -> (Int, Vec3) -> Maybe (Int, Vec3)
  cmp Nothing x = (Just x)
  cmp (Just (bp, ba)) (p, a) = if vabs ba < vabs a then (Just (bp, ba)) else (Just (p, a))
  in foldl cmp Nothing ps

runStep = let
  next (p, v, a) = let
    nv = vadd v a
    np = vadd p nv
    in (np, nv, a)
  pEq :: Particle -> Particle -> Bool
  pEq (p1, _, _) (p2, _, _) = p1 == p2
  remCols :: [Particle] -> [Particle]
  remCols [] = []
  remCols (x:xs) = let
    split :: ([Particle], [Particle]) -> Particle -> ([Particle], [Particle])
    split (cols, noncols) particle = let
      in if pEq x particle then ((particle:cols), noncols) else (cols, (particle:noncols))
    (cols, noncols) = foldl split ([], []) xs
    in if length cols > 0 then remCols noncols else x:remCols xs
  in remCols . map next

runSteps 0 ps = ps
runSteps x ps = runSteps (x-1) (runStep ps)

main = do
  contents <- getContents
  putStr (show $ minAcc $ zip [0..] [a | (p, v, a) <- parseInput contents])
  putStr "\n"
  putStr (show $ length $ runSteps 1000 $ parseInput contents)
