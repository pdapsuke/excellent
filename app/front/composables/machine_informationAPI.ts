// マシン情報作成時のリクエストボディの型定義
interface MachineInformationPost {
    ballspeed: string[]
    pitch_type: string[]
    batter_box: string
    username: string
    place_id: string
}

interface BreakingBall {
  id: number
  name: string
}


interface BallSpeed {
  id: number
  speed: number
}

// useBattingCenterApiの名前で関数をエクスポート
export const useMachineInformationApi = () => {
  return {
    // マシン情報の投稿
    async post(machine_information: MachineInformationPost) {
      return useApi().post<any>("postMachineInformation", "/machine_informations/", machine_information)
    },
    // マシン情報毎のあった！なかった！数を取得
    async get(machine_id: number, atta_nakatta: string) {
      return useApi().get<any>("getAttaCount", `/machine_informations/${machine_id}/atta_nakatta`, {"atta_nakatta": atta_nakatta})
    },
    // 球速一覧の取得
    async getBallSpeeds() {
      return useApi().get<BallSpeed>("getBallSpeeds", "/machine_configurations/ball_speeds")
    },
    // 球種一覧の取得
    async getBreakingBalls() {
      return useApi().get<BreakingBall>("getBreakingBalls", "/machine_configurations/breaking_balls")
    },
  }
}