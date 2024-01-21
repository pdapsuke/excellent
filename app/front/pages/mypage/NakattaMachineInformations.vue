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
		<v-table>
			<thead>
				<tr>
					<th class="text-left">球速 km/h</th>
					<th class="text-left">球種</th>
					<th class="text-left">打席</th>
					<th class="text-left">更新日</th>
					<th class="text-left">あった！数</th>
					<th class="text-left">あった！ボタン</th>
					<th class="text-left">なかった！数</th>
					<th class="text-left">なかった！ボタン</th>
					<th class="text-left"></th>
				</tr>
			</thead>
		</v-table>
	</div>
  </div>
</template>
