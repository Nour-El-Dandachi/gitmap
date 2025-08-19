<?php

namespace App\Http\Controllers\Common;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Laravel\Socialite\Facades\Socialite;
use App\Http\Controllers\Common\AuthController;

class GithubAuthController extends Controller
{

    public function redirect()
    {
        return Socialite::driver('github')->redirect();
    }

    public function callback()
    {

        //YOU SHOULD IMPLEMENT SERVICES TOMORROW !!!!!!!!!!!!!!
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

        return $this->responseJSON($user);
    }
}
