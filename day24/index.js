var fs = require('fs');
var PathFinder = require('geojson-path-finder');
var permutator = require('./permutator');

var grid = fs.readFileSync(process.argv[2], 'utf-8').split('\n');
var targets = [];
var features = [];

var handleState = function(x, y, wall, isFeature, coords, features) {
    var pushFeature = function() {
        features.push({
            type: 'Feature',
            geometry: {
                type: 'LineString',
                coordinates: coords.slice()
            }
        });

        coords.splice(0, coords.length);
    };
    var isWall = wall === '#';
    if (isFeature && isWall) {
        pushFeature();
    } else if (!isWall) {
        coords.push([x, y]);

        if (wall !== '.') {
            pushFeature()
        }

        coords.push([x, y]);

        return true;
    }

    return false;
}

var isFeature;
var coords = [];
for (var y = 0; y < grid.length; y++) {
    var line = grid[y];
    for (var x = 0; x < grid[y].length; x++) {
        isFeature = handleState(x, y, line[x], isFeature, coords, features);
        var square = line[x]
        if (square >= '0' && square <= '9') {
            var targetIndex = square.charCodeAt(0) - 48;
            while (targets.length <= targetIndex) targets.push(null);
            targets[targetIndex] = [x, y];
        }
    }
}

for (var x = 0; x < grid[0].length; x++) {
    for (var y = 0; y < grid.length; y++) {
        isFeature = handleState(x, y, grid[y][x], isFeature, coords, features);
    }
}

// console.log(JSON.stringify(features, null, 2));
// console.log(JSON.stringify(targets));

var pathFinder = new PathFinder({
    type: 'FeatureCollection',
    features: features
}, {
    weightFn: function(a, b) {
        var dx = a[0] - b[0];
        var dy = a[1] - b[1];
        return Math.sqrt(dx * dx + dy * dy);
    }
});

var costs = [];
for (var i = 0; i < targets.length; i++) {
    var pi = {type: 'Feature', geometry: {type: 'Point', coordinates: targets[i]}};
    var row = [];
    for (var j = 0; j < targets.length; j++) {
        // console.log('Calculating ' + i + ' to ' + j);
        if (i !== j) {
            var pj = {type: 'Feature', geometry: {type: 'Point', coordinates: targets[j]}};
            var p = pathFinder.findPath(pi, pj);
            if (p) {
                row.push(p);        
            } else {
                throw new Error('No path from ' + i + ' to ' + j);
            }
        } else {
            row.push(0);
        }
    }
    costs.push(row);
}

// console.log(JSON.stringify(costs, null, 2));

var targetNs = targets.map(function(_, i) { return i; }).slice(1);
var pathCost = function(targetIndices) {
    var cost = costs[0][targetIndices[0]].weight;
    for (var i = 1; i < targetIndices.length; i++) {
        cost += costs[targetIndices[i - 1]][targetIndices[i]].weight;
    }

    cost += costs[targetIndices[targetIndices.length - 1]][0].weight;

    return cost;
};
var best = permutator(targetNs).reduce(function(best, permutation) {
    cost = pathCost(permutation);

    if (cost < best.cost) {
        return {
            cost: cost,
            permutation: [permutation].concat(best.permutation)
        };
    } else if (cost === best.cost) {
        return {
            cost: cost,
            permutation: [permutation].concat(best.permutation)
        };
    }

    return best;
},
{
    path: [], 
    cost: Number.MAX_SAFE_INTEGER,
    permutation: []
});

console.log(best);
