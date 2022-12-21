using System.Globalization;

class Day12
{
    public static void Run()
    {
        var path = System.IO.Path.Join(AppDomain.CurrentDomain.BaseDirectory, "day12", "inputs.txt");
        //var path = System.IO.Path.Join(AppDomain.CurrentDomain.BaseDirectory, "day12", "test.txt");
        using var reader = new System.IO.StreamReader(path);

        var inputs = reader.ReadToEnd().Split("\r\n");
        Tuple<int, int> s = new(0, 0);
        Tuple<int, int> e = new(0, 0);
        for (int i = 0; i < inputs.Length; i++){
            if(inputs[i].IndexOf("S") > -1){
                s = new(i, inputs[i].IndexOf("S"));
            }
            if (inputs[i].IndexOf("E") > -1){
                e = new(i, inputs[i].IndexOf("E"));
            }
        }
        Console.WriteLine($"<{s}>, <{e}>");

        Node[,] OG_grid = Create_unvisited_set(inputs);
        List<int> results = new List<int> { };
        foreach (Node OG_node in OG_grid)
        {
            if (OG_node.value != 'a')
            {
                continue;
            }
            Node[,] grid = Create_unvisited_set(inputs);
            grid[OG_node.x, OG_node.y].distance = 0;
            grid[e.Item1, e.Item2].value = 'z';
            ref Node current_node = ref grid[s.Item1, s.Item2];
            while (true)
            {
                int[][] neighbours = current_node.Neighbours();
                foreach (int[] node in neighbours)
                {
                    if (node[0] < 0
                        | node[1] < 0
                        | node[0] > inputs.Length - 1
                        | node[1] > inputs[0].Length - 1)
                    {
                        continue;
                    }
                    ref Node neighbour = ref grid[node[0], node[1]];
                    if (neighbour.value <= current_node.value + 1)
                    {
                        int distance = current_node.distance + 1;
                        if (neighbour.distance > distance)
                        {
                            neighbour.distance = distance;
                        }
                    }

                }
                current_node.visited = true;
                if (grid[e.Item1, e.Item2].visited == true)
                {
                    break;
                }
                if (IsSmallestDitanceEqualInf(grid))
                {
                    break;
                }
                current_node = minimum_distance(grid);
            }
            int tmp = grid[e.Item1, e.Item2].distance;
            results.Add(grid[e.Item1, e.Item2].distance);
        }
        Console.WriteLine(results.Min());
    }

    static bool IsSmallestDitanceEqualInf(Node[,] grid)
    {
        int min = int.MaxValue;
        foreach(Node node in grid)
        {
            if (node.visited == false)
            {
                if(node.distance < min)
                {
                    min = node.distance;
                }
            }
        }
        if(int.MaxValue == min)
        {
            return true;
        }
        return false;
    }

    static Node minimum_distance(Node[,] grid)
    {
        int min = int.MaxValue;
        Node r_node = new Node();
        foreach(Node node in grid)
        {
            if(node.distance < min & node.visited == false)
            {
                r_node = node;
                min = node.distance;
            }
        }
        return r_node;
    }

    static Node[,] Create_unvisited_set(string[] matrix)
    {
        int y = matrix[0].Length;
        int x = matrix.Length;
        Node[,] unvisted_grid = new Node[x, y];
        for(int i = 0; i < x; i++)
        {
            for(int j = 0; j < y; j++)
            {
                unvisted_grid[i, j] = new Node(i, j, matrix[i][j]);
            }
        }
        return unvisted_grid;
    }
}

class Node
{
    public int distance = int.MaxValue;
    public bool visited = false;
    public int x;
    public int y;
    public char value;

    public Node(int x, int y, char v)
    {
        this.x = x;
        this.y = y;
        this.value = v;
    }

    public Node()
    {}

    public int[][] Neighbours()
    {
        return new int[][] { 
            new int[]{ this.x, this.y+1 },
            new int[]{ this.x, this.y-1 },
            new int[]{ this.x+1, this.y },
            new int[]{ this.x-1, this.y }
        };
    }
}