<?php

namespace App\Services\Common;
use App\Models\User;
use Laravel\Socialite\Facades\Socialite;

class GithubAuthService
{
    static function callback(){
        $githubUser = Socialite::driver('github')->user();

        $user = User::where('github_id', $githubUser->id)->first();

        if (!$user && $githubUser->email) {
            $existingUser = User::where('email', $githubUser->email)->first();

            if ($existingUser) {
                $existingUser->update([
                    'github_id'     => $githubUser->id,
                    'github_login'  => $githubUser->nickname,
                    'github_token'  => $githubUser->token,
                ]);

                $user = $existingUser->fresh();
            }
        }

        if (!$user) {
            $user = User::create([
                'name'          => $githubUser->name,
                'email'         => $githubUser->email,
                'github_id'     => $githubUser->id,
                'github_login'  => $githubUser->nickname,
                'github_token'  => $githubUser->token,
                'role'          => 'user',
            ]);
        }

        return $user;
    }
}
