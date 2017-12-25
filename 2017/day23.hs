import Data.List.Split
import Data.Char
import Text.Read
import qualified Data.Map.Strict as Map
import Data.Array

data Val = Reg Char | Lit Int deriving (Show)

data Instr = Snd Val
  | Set Val Val
  | Sub Val Val
  | Mul Val Val
  | Jnz Val Val
  deriving (Show)

execute :: (Array Int Instr) -> Int -> Map.Map Char Int -> Map.Map Char Int
execute p ip regs = if ip < 0 || ip > i then regs else e (p ! ip)
  where
    (0, i) = bounds p
    e :: Instr -> Map.Map Char Int
    e x = execute p nip ns
      where (ns, nip) = nextState x
    nextState :: Instr -> (Map.Map Char Int, Int)
    nextState (Set (Reg x) y) = (Map.insert x (eval y) regs, ip+1)
    nextState (Sub (Reg x) y) = (Map.insert x ((evalReg x) - (eval y)) regs, ip+1)
    nextState (Mul (Reg x) y) = (Map.adjust (\x -> x + 1) 'x' $ Map.insert x ((evalReg x) * (eval y)) regs, ip+1)
    nextState (Jnz x y) = if eval x /= 0 then (regs, ip+(eval y)) else (regs, ip+1)
    eval :: Val -> Int
    eval (Lit x) = x
    eval (Reg x) = Map.findWithDefault 0 x regs
    evalReg :: Char -> Int
    evalReg x = Map.findWithDefault 0 x regs

makeProgram lines = listArray (0, length lines - 1) $ map parseInstr lines

parseInstr = createInstr . splitOn " "
  where
    createInstr ["set", x, y] = Set (parseVal x) (parseVal y)
    createInstr ["sub", x, y] = Sub (parseVal x) (parseVal y)
    createInstr ["mul", x, y] = Mul (parseVal x) (parseVal y)
    createInstr ["jnz", x, y] = Jnz (parseVal x) (parseVal y)
    parseVal x = f (readMaybe x)
      where
        f (Just x) = Lit (x :: Int)
        f (Nothing) = Reg (head x)

main = do
  contents <- getContents
  putStr (show $ execute (makeProgram $ lines contents) 0 (Map.singleton 'x' 0))
  putStr ("\n")
  putStr (show $ execute (makeProgram $ lines contents) 0 (Map.fromList [('x', 0), ('a', 1)]))
  putStr ("\n")
