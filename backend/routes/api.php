<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Common\GithubAuthController;

Route::group(["prefix" =>"v0.1"], function(){
    

    Route::group(["prefix" => "guest"], function(){
        Route::get('/auth/github/redirect', [GithubAuthController::class, 'redirect']);
        Route::get('/auth/github/callback', [GithubAuthController::class, 'callback']);
    });
});