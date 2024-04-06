<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-10">
      <v-row class="justify-center">
        <NuxtLink :to="`/mypage/IttaBattingCenters`">行った！したバッティングセンター</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/PostedMachineInformations`">投稿したマシン情報</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/AttaMachineInformations`">あった！したマシン情報</NuxtLink>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <div class="font-weight-bold">なかった！したマシン情報</div>
        <v-divider class="border-opacity-90 mx-3" color="black" :thickness="1" vertical></v-divider>
        <NuxtLink :to="`/mypage/withdrawal`">アカウント削除</NuxtLink>
      </v-row>
    </div>
		<div class="mb-3">
			<div v-if="battingCenterAndMachines.length == 0">なかった！したマシン情報はありません</div>
      <div class="ma-10" v-else>
				<v-table>
					<thead>
						<tr>
							<th class="text-left">球速 km/h</th>
							<th class="text-left">球種</th>
							<th class="text-left">打席</th>
							<th class="text-left">更新日</th>
							<th class="text-left"></th>
							<th class="text-left"></th>
							<th class="text-left"></th>
						</tr>
					</thead>
					<tbody>
            <template v-for="batting_center in battingCenterAndMachines" :key=batting_center.id>
              <tr style="background: #eee;">
                <th colspan="7" class="text-center">
                  <NuxtLink :to="`/batting_centers/${batting_center.id}`">{{ batting_center.name }}</NuxtLink>
                </th>
              </tr>
              <template v-for="machine_information in batting_center.machine_informations">
                <tr>
                  <td>{{ machine_information.ball_speeds.map((x) => x.speed).join(", ") }}</td>
                  <td>{{ machine_information.breaking_balls.map((x) => x.name).join(", ") }}</td>
                  <td>{{ machine_information.batter_box }}</td>
                  <td>{{ useUtil().formatDate(machine_information.updated) }}</td>
                  <td>
                    <div class="d-flex justify-end align-center">
                      <div class="font-weight-bold text-secondary font-italic text-h6">{{ machine_information.atta_count }}</div>
                      <div>
                        <AttaButton
                          :atta="machine_information.atta"
                          @click="atta(batting_center.id, machine_information)"
                        ></AttaButton>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex justify-start align-center">
                      <div class="font-weight-bold text-secondary font-italic text-h6">{{ machine_information.nakatta_count }}</div>
                      <div>
                        <NakattaButton
                          :nakatta="machine_information.nakatta"
                          @click="nakatta(batting_center.id, machine_information)"
                        ></NakattaButton>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex justify-start">
                      <div>
                        <v-btn icon flat v-if="machine_information.is_owner==true"
                          @click="editDialog.open({
                            ball_speeds: ballSpeeds,
                            breaking_balls: breakingBalls,
                            batter_box: machine_information.batter_box,
                            selected_ball_speeds: useUtil().createSelectedBallSpeedsList(machine_information),
                            selected_breaking_balls: useUtil().createSelectedBreakingBallsList(machine_information),
                            battingCenterId: batting_center.id,
                            machineId: machine_information.id})"
                            ><v-icon color="warning" :icon="mdiNoteEditOutline"></v-icon>
                        </v-btn>
                      </div>
                      <div>
                        <v-btn icon flat v-if="machine_information.is_owner==true" @click="confirmDeletion.open({battingCenterId: batting_center.id, machineId: machine_information.id})">
                          <v-icon color="error" :icon="mdiDeleteForeverOutline"></v-icon>
                        </v-btn>
                      </div>
                    </div>
                  </td>
                </tr>
              </template>
            </template>
					</tbody>
				</v-table>
			</div>
		</div>
    <!-- 削除確認ダイアログ -->
    <ConfirmDialog
      title="マシン情報の削除"
      message="本当に削除しますか"
      confirmBtn="削除"
      cancelBtn="キャンセル"
      colorCancel="black"
      colorConfirm="error"
      ref="confirmDeletion"
      @confirm="deleteMachineInformation">
    </ConfirmDialog>
    <!-- 編集確認ダイアログ -->
    <EditDialog
      title="マシン情報の編集"
      confirmBtn="OK"
      cancelBtn="キャンセル"
      colorCancel="black"
      colorConfirm="error"
      ref="editDialog"
      @confirm="editMachineInformation">
    </EditDialog>
  </div>
</template>

<script setup lang="ts">
import { mdiNoteEditOutline, mdiDeleteForeverOutline } from '@mdi/js'

// ミドルウェアによるログインチェック
definePageMeta({ middleware: ["auth"] })

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

interface UpdateAttaNakattaResponse{
  id: number
  atta_count: number
  nakatta_count: number
  atta: boolean
  nakatta: boolean
}

interface BattingCenterAndMachines {
  id: number
  place_id: string
  name: string
  formatted_address: string
  machine_informations: MachineInformation[]
}

const alert = ref<any>(null)
const confirmDeletion = ref<any>(null)
const editDialog = ref<any>(null)

let batterBox = ref<string>()
let battingCenterAndMachines = ref<BattingCenterAndMachines[]>()
let selectedBallSpeeds = ref<number[]>([])
let selectedBreakingBalls = ref<number[]>([])
let attaNakattaUpdateResponse = ref<UpdateAttaNakattaResponse>()
let attaNakattaUpdateError = ref<any>()

// 投稿したマシン情報と関連するバッティングセンターの一覧を取得
const { data, error, refresh } = await useUserApi().getMyNakattaMachines()
// 一覧に失敗した場合、アラートとログを出力
if (!data.value || error.value) {
  alert.value.error(error.value)
  console.error(error.value)
} else {
  battingCenterAndMachines.value = data.value
}

const { data: ballSpeeds, error: ballSpeedsError } = await useMachineInformationApi().getBallSpeeds()
// 球速一覧の取得に失敗した場合、アラートとログを出力
if (!ballSpeeds.value || ballSpeedsError.value) {
  alert.value.error(ballSpeedsError.value)
  console.error(ballSpeedsError.value)
}

const { data: breakingBalls, error: breakingBallsError } = await useMachineInformationApi().getBreakingBalls()
// 球種一覧の取得に失敗した場合、アラートとログを出力
if (!breakingBalls.value || breakingBallsError.value) {
  alert.value.error(breakingBallsError.value)
  console.error(breakingBallsError.value)
}

// あった！フラグに応じてあった！を登録/解除
async function atta(battingCenterId: number, machineInformation: MachineInformation) {
  // あった！フラグがfalseの場合、あった！ユーザーの追加
  if (machineInformation.atta == false) {
    ({ data: attaNakattaUpdateResponse, error: attaNakattaUpdateError } =  await useMachineInformationApi().addAttaUser(battingCenterId, machineInformation.id))

  // あった！フラグがtrueの場合、あった！ユーザーの削除
  } else if (machineInformation.atta == true) {
    ({ data: attaNakattaUpdateResponse, error: attaNakattaUpdateError } =  await useMachineInformationApi().removeAttaUser(battingCenterId, machineInformation.id))

  // あった！フラグがtrue, false以外の場合、エラー出力
  } else {
    alert.value.error("Bad Request")
    console.error("Bad Request")
    return
  }

  if (!attaNakattaUpdateResponse.value || attaNakattaUpdateError.value) {
    alert.value.error(attaNakattaUpdateError.value)
    console.error(attaNakattaUpdateError.value)
    return
  }

  useUtil().updateAttaNakattaForBattingCenterAndMachines(battingCenterId, battingCenterAndMachines.value, machineInformation, attaNakattaUpdateResponse.value)
}

// なかった！フラグに応じてなかった！を登録/解除
async function nakatta(battingCenterId: number, machineInformation: MachineInformation) {
  // なかった！フラグがfalseの場合、なかった！ユーザーの追加
  if (machineInformation.nakatta == false) {
    ({ data: attaNakattaUpdateResponse, error: attaNakattaUpdateError } =  await useMachineInformationApi().addNakattaUser(battingCenterId, machineInformation.id))

  // なかった！フラグがtrueの場合、なかった！ユーザーの削除
  } else if (machineInformation.nakatta == true) {
    ({ data: attaNakattaUpdateResponse, error: attaNakattaUpdateError } =  await useMachineInformationApi().removeNakattaUser(battingCenterId, machineInformation.id))

  // なかった！フラグがtrue, false以外の場合、エラー出力
  } else {
    alert.value.error("Bad Request")
    console.error("Bad Request")
    return
  }

  if (!attaNakattaUpdateResponse.value || attaNakattaUpdateError.value) {
    alert.value.error(attaNakattaUpdateError.value)
    console.error(attaNakattaUpdateError.value)
    return
  }

  useUtil().updateAttaNakattaForBattingCenterAndMachines(battingCenterId, battingCenterAndMachines.value, machineInformation, attaNakattaUpdateResponse.value)
}


async function deleteMachineInformation(confirm: boolean, parameters: any) {
  // キャンセルされた場合は何もしない
  if (!confirm) { return }
  // マシン情報削除APIを呼び出す
  const { error } = await useMachineInformationApi().deleteMachineInformation(parameters.battingCenterId, parameters.machineId)

  if (error.value instanceof Error) {
    alert.value.error(error.value)
    console.error(error.value)
    return
  }
  // 成功: マシン情報一覧を更新
  await refresh()

	if (!data.value || error.value) {
  alert.value.error(error.value)
  console.error(error.value)
	} else {
  battingCenterAndMachines.value = data.value
	}
}

async function editMachineInformation(
  confirm: boolean,
  parameters: any,
  selectedBatterBox: number[],
  selectedBallSpeeds: number[],
  selectedBreakingBalls: number[],
) {
  // キャンセルされた場合は何もしない
  if (!confirm) { return }
  // マシン情報更新APIを呼び出す
  const { data: updateMachineInformationResponse, error: updateMachineInformationError } = await useMachineInformationApi().updateMachineInformation(
    parameters.battingCenterId,
    parameters.machineId,
    {
      ballspeed_ids: selectedBallSpeeds,
      breaking_ball_ids: selectedBreakingBalls,
      batter_box: selectedBatterBox,
    })

  if (updateMachineInformationError.value instanceof Error) {
    alert.value.error(updateMachineInformationError.value)
    console.error(updateMachineInformationError.value)
    return
  }

	await refresh()

	if (!data.value || error.value) {
  alert.value.error(error.value)
  console.error(error.value)
	} else {
  battingCenterAndMachines.value = data.value
	}
}
</script>
