import qualified Text.Regex as Re
import qualified Data.Map.Strict as Map
import Debug.Trace

type Instr = (Bool, Int, Char)
type StateDef = Map.Map Bool Instr
type Program = Map.Map Char StateDef
type Tape = Map.Map Int Bool
type State = (Program, Tape, Int, Char)

charToBool "0" = False
charToBool "1" = True

dirToInt "left" = -1
dirToInt "right" = 1

boolToInt False = 0
boolToInt True = 1

parseStateDef :: [String] -> ([String], Char, StateDef)
parseStateDef ls = (drop 9 ls, parseStateLabel $ head ls, parseInstrs $ drop 1 ls)
  where
    parseStateLabel l = head label
      where 
        (Just [label]) = Re.matchRegex stateLabelExp l
        stateLabelExp = Re.mkRegex "^In state ([A-Z]):$"
    parseInstrs ls = Map.fromList [parseInstr $ take 4 ls, parseInstr $ take 4 $ drop 4 ls]
    parseInstr ls = (parseTapeState $ head ls, parseStateInstr $ drop 1 ls)
    parseTapeState l = charToBool state
      where 
        (Just [state]) = Re.matchRegex tapeStateExp l
        tapeStateExp = Re.mkRegex "^ *If the current value is (0|1):$"
    parseStateInstr ls = (parseWrite $ head ls, parseMove $ head $ drop 1 ls, parseNextState $ head $ drop 2 ls)
    parseWrite l = charToBool write
      where 
        (Just [write]) = Re.matchRegex writeExp l
        writeExp = Re.mkRegex "^ *- Write the value (0|1).$"
    parseMove l = dirToInt move
      where 
        (Just [move]) = Re.matchRegex moveExp l
        moveExp = Re.mkRegex "^ *- Move one slot to the (left|right).$"
    parseNextState l = head nextState
      where 
        (Just [nextState]) = Re.matchRegex nextStateExp l
        nextStateExp = Re.mkRegex "^ *- Continue with state ([A-Z]).$"

parseState :: [String] -> (State, Int)
parseState ls = ((Map.fromList $ parseStateDefs stateDefLines, Map.empty, 0, initialStateLabel), steps)
  where
    nonEmpty = filter (\x -> x /= "") ls
    stateDefLines = drop 2 nonEmpty
    parseStateDefs [] = []
    parseStateDefs ls = (stateLabel, stateDef):(parseStateDefs remaining)
      where (remaining, stateLabel, stateDef) = parseStateDef ls
    (initialStateLabel, steps) = parseInitialState nonEmpty
    parseInitialState ls = (parseInitialStateLabel $ head ls, parseSteps $ head $ drop 1 ls)
    -- parseInitialStateLabel l | trace l False=undefined
    parseInitialStateLabel l = head stateLabel
      where 
        (Just [stateLabel]) = Re.matchRegex initialStateLabelExp l
        initialStateLabelExp = Re.mkRegex "^Begin in state ([A-Z]).$"
    parseSteps l = read steps :: Int
      where 
        (Just [steps]) = Re.matchRegex stepsExp l
        stepsExp = Re.mkRegex "^Perform a diagnostic checksum after ([0-9]+) steps.$"

step :: State -> State
step (program, tape, pos, label) = (program, Map.insert pos newValue tape, pos+move, nextLabel)
  where
    Just stateDef = Map.lookup label program
    currentValue = Map.findWithDefault False pos tape
    Just (newValue, move, nextLabel) = Map.lookup currentValue stateDef

runSteps (state, steps)
  | steps > 0 = runSteps (step state, steps - 1)
  | otherwise = state

checksum (_, tape, _, _) = foldl (+) 0 $ map (boolToInt . snd) $ Map.toList tape

main = do
  contents <- getContents
  putStr (show $ checksum $ runSteps $ parseState $ lines contents)
  putStr "\n"
