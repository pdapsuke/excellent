interface BattingCenter {
  id: number
  place_id: string
  name: string
  formatted_address: string
  photos: any[] | undefined
  itta_count: number
  itta: string
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
  atta: string
  nakatta_count: number
  nakatta: string
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
    // 行った！したバッティングセンターの取得
    async getMyIttaBattingCenters() {
      return useApi().get<BattingCenter>("getMyIttaBattingCenters", "/users/me/itta_centers")
    },
    // 投稿したマシン情報の取得
    async getMyPostedMachines() {
      return useApi().get<BattingCenterAndMachines[]>("getMyPostedMachines", "/users/me/posted_machine_informations")
    }
  }
}