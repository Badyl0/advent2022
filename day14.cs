using System.Data;
using System.Drawing;
using System.Globalization;
using System.Security.Cryptography.X509Certificates;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Serialization;

class Day14
{
    public static void Run()
    {
        var path = System.IO.Path.Join(AppDomain.CurrentDomain.BaseDirectory, "day14", "inputs.txt");
        //var path = System.IO.Path.Join(AppDomain.CurrentDomain.BaseDirectory, "day14", "test.txt");
        List<List<char>> cave = new();
        cave.Add(new List<char> {'.'});
        foreach (string line in System.IO.File.ReadLines(path))
        {
            string[] points = line.Split(" -> ");
            System.Collections.IEnumerator points_enum =  points.GetEnumerator();
            points_enum.MoveNext();
            Point current = MakePoint(points_enum);
            PutStone(current, cave);
            Point next;
            while (true)
            {
                if (points_enum.MoveNext())
                {
                    next = MakePoint(points_enum);
                    PutWall(current, next, cave);
                }
                else
                {
                    break;
                }
                current = next;
            }
            //Console.WriteLine("boom");
        }
        AddFloor(cave);
        AlignCave(cave);
        //PrintCave(cave);
        int rested = 0;
        while(true)
        {
            Sand sand = DropSand();
            while (sand.IsFalling() & !sand.inf)
            {
                sand.FreeFall(cave);
            }
            if (sand.rest & sand.coords.X == 500 & sand.coords.Y == 0)
            {
                rested++;
                break;
            }
            rested++;
        }   
        Console.WriteLine(rested);
        PrintCave(cave);

    }

    private static void AddFloor(List<List<char>> cave)
    {
        int max_size = cave.Max(x => x.Count);
        //cave.Add(new List<char> {'.'});
        Point current = new Point(0, cave.Count + 1);
        Point next = new Point(max_size+max_size, cave.Count + 1);
        PutWall(current, next, cave);
    }

    private static void AlignCave(List<List<char>> cave)
    {
        int max_size = cave.Max(x => x.Count);
        //Console.WriteLine(max_size);
        foreach(List<char> row in cave)
        {
            while(row.Count < max_size)
            {
                row.Add('.');
            }
        }
       
    }

    private static void PrintCave(List<List<char>> cave)
    {
        //int start = -1, end=-1;
        foreach (List<char> row in cave)
        {
            //    if (row.Contains('#') | row.Contains('o'))
            //    {
            //        start = row.IndexOf('#');
            //        if (start > -1 | row.IndexOf('o') > -1)
            //        {
            //            if(start > row.IndexOf('o'))
            //            start = row.IndexOf('o');
            //        }
            //        end = row.LastIndexOf('#');
            //        if (end < row.IndexOf('o'))
            //        {
            //            end = row.LastIndexOf('o');
            //        }
            //    }
            //    //if (start < 1000 & end > 0)
            //    //{
            //    //    Console.WriteLine(string.Join("", row));
            //    //}
            int max_size = row.Count;
            Console.WriteLine(string.Join("", row.GetRange(488, 30)));
        }
    }

    private static Sand DropSand()
    {
        return new Sand();
    }

    private static void PutWall(Point current, Point next, List<List<char>> cave)
    {
        Point vector = new();
        switch(current.X - next.X, current.Y - next.Y) {
            case ( > 0, > 0): // NW
                vector.X = -1;
                vector.Y = -1;
                break;
            case ( < 0, > 0): //NE
                vector.X = 1;
                vector.Y = -1;
                break;
            case ( > 0, < 0): // SW
                vector.X = -1;
                vector.Y = 1;
                break;
            case ( < 0, < 0): //SE
                vector.X = 1;
                vector.Y = 1;
                break;
            case (0, < 0): //S
                vector.X = 0;
                vector.Y = 1;
                break;
            case (0, > 0): //N
                vector.X = 0;
                vector.Y = -1;
                break;
            case (< 0, 0): //E
                vector.X = 1;
                vector.Y = 0;
                break;
            case (> 0, 0): //W
                vector.X = -1;
                vector.Y = 0;
                break;
        }
        while(current != next)
        {
            PutStone(current, cave);
            current.Offset(vector);
        }
        PutStone(current, cave);
    }

    private static void PutStone(Point current, List<List<char>> cave)
    {
        List<char> row;
        try {
            row = cave[current.Y];
        }catch(ArgumentOutOfRangeException) { 
            while(cave.Count <= current.Y) {
                cave.Add(new List<char> { '.' });
            }
            row = cave[current.Y];
        }
        try { 
            row[current.X] = '#';
        }
        catch(ArgumentOutOfRangeException) {
            while (row.Count <= current.X){
                row.Add('.');
            }
            row[current.X] = '#';
        }
    }

    public static void PutSand(Point current, List<List<char>> cave)
    {
        cave[current.Y][current.X] = 'o';
    }

    private static Point MakePoint(System.Collections.IEnumerator points_enum)
    {
        string[] x_y = points_enum.Current.ToString().Split(",");
        Point current = new Point(Int32.Parse(x_y[0]), Int32.Parse(x_y[1]));
        return current;
    }
}

class Sand
{
    public Point coords;
    public bool rest;
    public bool inf;
    public Sand() {
        this.coords = new(500, 0);
        this.rest = false;
        this.inf = false;
    }

    internal bool IsFalling()
    {
        return !this.rest;
    }

    internal void FreeFall(List<List<char>> cave)
    {
        Point vector = new Point(0,0);
        try
        {
            if (cave[this.coords.Y + 1][this.coords.X] == '.')
            {
                vector = new Point(0, 1);
            }
            else if (cave[this.coords.Y + 1][this.coords.X - 1] == '.')
            {
                vector = new Point(-1, 1); // NW
            }
            else if (cave[this.coords.Y + 1][this.coords.X + 1] == '.')
            {
                vector = new Point(1, 1); // NE
            }
            else
            {
                this.rest = true;
                Day14.PutSand(this.coords, cave);
            }
        }
        catch (ArgumentOutOfRangeException)
        {
            this.inf = true;
        }
        if (!vector.IsEmpty) {
            this.coords.Offset(vector!);
        }
    }
}