import tkinter as tk
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["计算机网络-课设"]

class App:
    def __init__(self, master):
        self.master = master
        master.title("省份分数线查询")

        # 添加标签和选择框
        self.province_label = tk.Label(master, text="省份:")
        self.province_label.grid(column=0, row=0)
        self.province_combo = tk.StringVar()
        provinces = db.list_collection_names()
        province_options = tuple(provinces)
        self.province_combo.set(province_options[0])
        self.province_dropdown = tk.OptionMenu(master, self.province_combo, *province_options)
        self.province_dropdown.grid(column=1, row=0)

        # 添加表格
        self.table = tk.Listbox(master, height=10, width=60)
        self.table.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

        self.search_button = tk.Button(master, text="查询", command=self.show_results)
        self.search_button.grid(column=0, row=2)

        self.reset_button = tk.Button(master, text="重置", command=self.reset)
        self.reset_button.grid(column=1, row=2)

        self.table_data = []

    def show_results(self):
        province_data = self.province_combo.get()
        province = province_data[province_data.index(".") + 1:]
        data_list = []
        for coll_name in db.list_collection_names():
            collection = db[coll_name]
            query = {"地区": province}
            result = collection.find(query, {"_id": 0, "批次": 1, "分数线": 1, "位次": 1})
            for item in result:
                data_list.append(f"{province}   {item['分数线']}      {item['位次']}   {item['批次']} ")

        # 清空表格数据并保存新的查询结果
        self.table.delete(0, "end")
        if data_list:
            self.table_data = ["省份    分数线     位次       批次 "]
            for item in data_list:
                self.table_data.append(item)
        else:
            self.table_data = ["没有找到该省份的数据"]
        self.show_table()

    def reset(self):
        # 清空表格数据并允许用户重新输入省份名称
        self.table_data = []
        self.table.delete(0, "end")
        self.province_dropdown.configure(state="normal")

    def show_table(self):
        # 显示保存的表格数据
        for item in self.table_data:
            self.table.insert("end", item)
        # 禁用省份选择框，防止用户修改查询条件
        self.province_dropdown.configure(state="disabled")


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()