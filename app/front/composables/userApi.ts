interface BattingCenter {
  id: number
  place_id: string
  name: string
  formatted_address: string
  photos: any[] | undefined
  itta_count: number
  itta: boolean
}

interface BreakingBall {
  id: number
  name: string
}

interface BallSpeed {
  id: number
  speed: number
}

interface MachineInformation{
  id: number
  is_owner: boolean
  breaking_balls: BreakingBall[]
  ball_speeds: BallSpeed[]
  atta_count: number
  atta: boolean
  nakatta_count: number
  nakatta: boolean
  updated: string
}

interface BattingCenterAndMachines {
  id: number
  place_id: string
  name: string
  formatted_address: string
  machine_informations: MachineInformation[]
}

// useUserApiの名前で関数をエクスポート
export const useUserApi = () => {
  return {
    // ユーザーサインイン
    async signIn(token: string) {
      return useApi().post<any>("signInUser", "/users/signin", {}, {"Authorization": `Bearer ${token}`})
    },
    // ユーザー(DB管理)削除
    async deleteUser(email: string) {
      return useApi().delete<any>("deleteUser", "/users", {"email": email})
    },
    // トークン検証
    async validateToken(token: string) {
      return useApi().post<any>("validateToken", "/users/me/token", {"id_token": `${token}`})
    },
    // 行った！したバッティングセンターの取得
    async getMyIttaBattingCenters() {
      return useApi().get<BattingCenter>("getMyIttaBattingCenters", "/users/me/itta_centers")
    },
    // 投稿したマシン情報の取得
    async getMyPostedMachines() {
      return useApi().get<BattingCenterAndMachines[]>("getMyPostedMachines", "/users/me/posted_machine_informations")
    },
    // 投稿したマシン情報の取得
    async getMyAttaMachines() {
      return useApi().get<BattingCenterAndMachines[]>("getMyAttaMachines", "/users/me/atta_machine_informations")
    },
    // 投稿したマシン情報の取得
    async getMyNakattaMachines() {
      return useApi().get<BattingCenterAndMachines[]>("getMyNakattaMachines", "/users/me/nakatta_machine_informations")
    }
  }
}