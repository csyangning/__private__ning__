using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using CLAP;

namespace fyf
{
    public class Apps
    {
        [Verb(IsDefault = true)]
        public static void MergeCSV(string folderName)
        {
            if (!Directory.Exists(folderName))
            {
                Console.WriteLine("Folder {0} doesn't!", folderName);
            }

            string resultFolder = Path.Combine(folderName, "Result");
            if (!Directory.Exists(resultFolder))
            {
                Directory.CreateDirectory(resultFolder);
            }

            Console.WriteLine("Result will be saved to {0}", resultFolder);

            foreach (string fileName in Directory.GetFiles(folderName))
            {
                Console.WriteLine("Processing file: {0}", fileName);
                string[] fileContent = File.ReadAllLines(fileName);
                Dictionary<string, List<string>> resultDictionary = new Dictionary<string, List<string>>();
                resultDictionary.Add("Name", new List<string>());
                bool headerMode = false;
                bool resultMode = false;

                for (int i = 0; i < fileContent.Length; i++)
                {
                    if (string.IsNullOrEmpty(fileContent[i]))
                    {
                        continue;
                    }

                    if (fileContent[i].Contains("Header"))
                    {
                        resultDictionary["Name"].Add(fileContent[i + 3].Trim(','));
                        i = i + 3;
                        headerMode = true;
                        resultMode = false;
                        continue;
                    }

                    if (fileContent[i].Contains("Result"))
                    {
                        headerMode = false;
                        if (resultMode)
                        {
                            resultDictionary["Name"].Add(" ");
                        }
                        else
                        {
                            resultMode = true;
                        }
                        continue;
                    }

                    if (!headerMode)
                    {
                        string[] result = fileContent[i].Split(',');
                        if (!resultDictionary.ContainsKey(result[0]))
                        {
                            resultDictionary.Add(result[0], new List<string>());
                        }

                        resultDictionary[result[0]].Add(result[1]);
                    }
                }

                StringBuilder stringBuilder = new StringBuilder();
                foreach (string key in resultDictionary.Keys)
                {
                    stringBuilder.AppendLine(string.Format("{0},{1}", key, string.Join(",", resultDictionary[key])));
                }

                File.WriteAllText(Path.Combine(resultFolder, Path.GetFileName(fileName)), stringBuilder.ToString());
            }

            Console.WriteLine("Done");
        }
    }
}