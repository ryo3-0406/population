import pandas as pd


# df_setai = pd.read_excel("./data/R2_pop_setai.xlsx")
# df_age = pd.read_excel("./data/R2_pop_age.xlsx")

# df_setai.to_pickle("./data/R2_pop_setai.pickle")
# df_age.to_pickle("./data/R2_pop_age.pickle")


class Population:
    def __init__(self):
        df_age = pd.read_pickle("./data/R2_pop_age.pickle")
        df_age = df_age[df_age["code_2"] == 000]

        df_setai = pd.read_pickle("./data/R2_pop_setai.pickle")
        df_setai = df_setai[df_setai["code_2"] == 000]

        self.df_age = df_age
        self.df_setai = df_setai

    def age_area_population(self, age_min, age_max, area, sex, flag_japaneze=1):
        df = self.df_age.copy()
        df = df[df["地域名"].isin(area)]
        df = df[df["sex"] == sex]

        if flag_japaneze:
            df = df[df["国籍総数か日本人"] == "1_うち日本人"]
        else:
            df = df[df["国籍総数か日本人"] == "0_国籍総数"]


        df = df.loc[:, age_min:age_max]
        result = df.sum(axis=1).sum()

        return result

    def household_count(self, area):
        df = self.df_setai.copy()
        df = df[df["地域名"].isin(area)]
        df = df["0_総数"]

        result = df.sum()


        return result

    def area_list(self, flag_household=0):

        if flag_household:
            df = self.df_setai
        else:
            df = self.df_age

        area_list = df["地域名"].unique().tolist()

        return area_list


# model = Population()
# model.age_area_population(age_min=20, age_max=30, area=["北海道", "青森県", "岩手県"], sex="男女", flag_japaneze=0)
# model.household_count(area=["北海道", "青森県"])