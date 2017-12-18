import Data.List.Split
import Data.Char
import Text.Read
import qualified Data.Map.Strict as Map
import Data.Array

data Val = Reg Char | Lit Int deriving (Show)

data Instr = Snd Val
  | Set Val Val
  | Add Val Val
  | Mul Val Val
  | Mod Val Val
  | Rcv Val
  | Jgz Val Val
  deriving (Show)

execute :: (Array Int Instr) -> Int -> Map.Map Char Int -> Int
execute p ip regs = e (p ! ip)
  where
    e :: Instr -> Int
    e (Rcv y) = if eval y > 0 then evalReg '_' else execute p (ip+1) regs
    e x = execute p nip ns
      where (ns, nip) = nextState x
    nextState :: Instr -> (Map.Map Char Int, Int)
    nextState (Set (Reg x) y) = (Map.insert x (eval y) regs, ip+1)
    nextState (Add (Reg x) y) = (Map.insert x ((evalReg x) + (eval y)) regs, ip+1)
    nextState (Mul (Reg x) y) = (Map.insert x ((evalReg x) * (eval y)) regs, ip+1)
    nextState (Mod (Reg x) y) = (Map.insert x ((evalReg x) `mod` (eval y)) regs, ip+1)
    -- nextState (Rcv y) = if (eval y) > 0 then (Map.findWithDefault 0 "freq" regs) else regs
    nextState (Snd y) = (Map.insert '_' (eval y) regs, ip+1)
    nextState (Jgz x y) = if eval x > 0 then (regs, ip+(eval y)) else (regs, ip+1)
    eval :: Val -> Int
    eval (Lit x) = x
    eval (Reg x) = Map.findWithDefault 0 x regs
    evalReg :: Char -> Int
    evalReg x = Map.findWithDefault 0 x regs

makeProgram lines = listArray (0, length lines - 1) $ map parseInstr lines

parseInstr = createInstr . splitOn " "
  where
    createInstr ["set", x, y] = Set (parseVal x) (parseVal y)
    createInstr ["add", x, y] = Add (parseVal x) (parseVal y)
    createInstr ["mul", x, y] = Mul (parseVal x) (parseVal y)
    createInstr ["mod", x, y] = Mod (parseVal x) (parseVal y)
    createInstr ["jgz", x, y] = Jgz (parseVal x) (parseVal y)
    createInstr ["rcv", x] = Rcv (parseVal x)
    createInstr ["snd", x] = Snd (parseVal x)
    parseVal x = f (readMaybe x)
      where
        f (Just x) = Lit (x :: Int)
        f (Nothing) = Reg (head x)

main = do
  contents <- getContents
  putStr (show $ execute (makeProgram $ lines contents) 0 Map.empty)
  putStr ("\n")
