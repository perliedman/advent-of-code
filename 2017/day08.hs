import qualified Text.Regex as Re
import Data.Maybe
import Data.List.Split
import qualified Data.Map.Strict as Map
import Debug.Trace

type State = Map.Map String Int
type CmpFunc = State -> Arg -> Arg -> Bool
data Register = Register String deriving (Show)
data Arg = RegArg Register | Literal Int deriving (Show)
data Operand = Inc Register Arg | Dec Register Arg deriving (Show)
data Conditional = Conditional Arg CmpFunc Arg
data Instruction = Instruction Operand Conditional

lineExp = Re.mkRegex "^([a-z]+) +(inc|dec) +((-|)[0-9]+) +if +([a-z]+) ([!<>=]+) +((-|)[0-9]+)$"
regExp = Re.mkRegex "^([a-z]+)$"
valExp = Re.mkRegex "^((-|)[0-9]+)$"

val s (RegArg (Register r)) = Map.findWithDefault 0 r s
val s (Literal l) = l

parseRegister x = Register x

-- parseArg x | trace ("trace " ++ show x) False = undefined
parseArg x = let
  regMatch = Re.matchRegex regExp x
  valMatch = Re.matchRegex valExp x
  -- make a b | trace ("make " ++ show a ++ " " ++ show b) False = undefined
  make Nothing (Just [val, _]) = Literal (read val :: Int) 
  make (Just [reg]) Nothing = RegArg (parseRegister reg)
  in make regMatch valMatch

parseComparison x
  | x == "==" = makeComp (==)
  | x == "!=" = makeComp (/=)
  | x == "<" = makeComp (<)
  | x == ">" = makeComp (>)
  | x == "<=" = makeComp (<=)
  | x == ">=" = makeComp (>=)
  where makeComp f = (\s x y -> f (val s x) (val s y))

parseOp reg op val
  | op == "inc" = Inc (parseRegister reg) (parseArg val)
  | op == "dec" = Dec (parseRegister reg) (parseArg val)  

parseCondition reg op val = Conditional (parseArg reg) (parseComparison op) (parseArg val)

parseStatement [opReg, op, opVal, _, condReg, condOp, condVal, _] =
  Instruction (parseOp opReg op opVal) (parseCondition condReg condOp condVal)
parseInput input = map fromJust $ map (Re.matchRegex lineExp) $ lines input

eval :: State -> Conditional -> Bool
eval state (Conditional arg1 cmp arg2) = cmp state arg1 arg2

inc :: State -> String -> Int -> State
inc state r v = Map.insert r ((+) v (Map.findWithDefault 0 r state)) state

maxReg state = maximum $ map snd $ Map.toList state

updateState :: State -> Operand -> State
updateState state (Inc (Register r) arg) = inc state r (val state arg)
updateState state (Dec (Register r) arg) = inc state r (-(val state arg))

execute :: [Instruction] -> State -> Int -> (State, Int)
execute [] state hi = (state, max hi $ maxReg state)
execute ((Instruction op cond):xs) state hi = let
  nextState = if eval state cond then updateState state op else state
  nextHi = max hi $ maxReg nextState
  in execute xs nextState nextHi

a contents = maxReg $ fst $ execute (map parseStatement $ (parseInput contents)) Map.empty 0
b contents = snd $ execute (map parseStatement $ (parseInput contents)) Map.empty 0

main = do
  contents <- getContents
  putStr("A: ")
  putStr(show (a contents))
  putStr("\n")
  putStr("B: ")
  putStr(show (b contents))
  putStr("\n")
  -- putStr(show $ execute (map parseStatement $ (parseInput contents)) Map.empty)
  -- putStr(show $ parseInput contents)
