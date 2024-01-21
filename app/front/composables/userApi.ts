interface BattingCenter {
  id: number
  place_id: string
  name: string
  formatted_address: string
  photos: any[] | undefined
  itta_count: number
  itta: string
}

// useUserApiの名前で関数をエクスポート
export const useUserApi = () => {
  return {
    // ユーザーサインイン
    async signIn(token: string) {
      return useApi().post<any>("signInUser", "/users/signin", {}, {"Authorization": `Bearer ${token}`})
    },
    // 行った！したバッティングセンターの取得
    async getMyIttaBattingCenters() {
      return useApi().get<BattingCenter>("getMyIttaBattingCenters", "/users/me/itta_centers")
    }
  }
}